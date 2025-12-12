import json
import numpy as np
import math
from scipy.stats import chi2
from scipy.optimize import minimize
import random

"""1. Проверка гипотезы о виде распределения"""

#p = 0.45
m = 14
#t = 1/8

"""КРИТЕРИЙ СОГЛАСИЯ КОЛМОГОРОВА(СМИРНОВА) ДЛЯ СЛОЖНОЙ ГИПОТЕЗЫ"""

a = 0.05

# Моделирование случайной величины
def erlang_rand_variable(m, t):
    k = 0
    for _ in range(m):
        s = random.random()
        while s == 0:
            s = random.random()
        k += -math.log(s) / t
    return k

# Процедура получения выборки размера n
def erlang_sample(n, t):
    sample = []
    for i in range(n):
        k = erlang_rand_variable(m, t)
        sample.append(k)
    return sample

#Оценка параметра
def omp_parameter_k(sample):
    param = m / np.mean(sample)
    return param

#Вычисление статистики Колмогорова для простой гипотезы
def kolmogorov_statistic(sample, param):
    n = len(sample)
    D_plus = 0
    D_minus = 0
    sorted_sample = sorted(sample)

    t = param
    for k in range(1, n + 1):
        k_value = sorted_sample[k - 1]
        sum_term = 0
        for i in range(m):
            sum_term += (t * k_value) ** i / math.factorial(i)
        F = 1 - math.exp(-t * k_value) * sum_term
        D_plus = max(D_plus, abs(k / n - F))
        D_minus = max(D_minus, abs(F - (k - 1) / n))

    D = max(D_plus, D_minus)
    return D

#Проверка сложной гипотезы методом компьютерного анализа
def complex_kolmogorov_test(sample, N):

    n = len(sample)
    param = omp_parameter_k(sample) #оценка параметра по исходной выборке

    D_obs = kolmogorov_statistic(sample, param) #Вычисление статистики Dn*

    D_sim = [] #генерация выборок, оценка их параметров, вычисление статистик
    for i in range(N):
        sample_simulated = erlang_sample(n, param)

        param_simulated = omp_parameter_k(sample_simulated)
        D_simulated = kolmogorov_statistic(sample_simulated, param_simulated)
        D_sim.append(D_simulated)

    D_sim_sorted = np.sort(D_sim) #Построение эмпирической функции распределения и вычисление вероятности
    G = np.sum(D_sim_sorted < D_obs) / N
    P = 1 - G

    return param, P

"""КРИТЕРИЙ СОГЛАСИЯ ХИ-КВАДРАТ ДЛЯ СЛОЖНОЙ ГИПОТЕЗЫ"""

#Оценка параметра
def omp_grouped_parameter_x(distribution, intervals, frequency):

    n = sum(frequency) #общее количество наблюдений
    if distribution == 'geometric':
        def log_L(p_arr): #логарифм функции правдоподобия
            p = float(p_arr[0])
            logL = 0
            for i in range(len(frequency)):
                if intervals[i] > 0:
                    F_a = 1 - (1 - p) ** intervals[i]
                else:
                    F_a = 0
                F_b = 1 - (1 - p) ** intervals[i + 1]
                probability = max(F_b - F_a, 1e-10)
                logL += frequency[i] * math.log(probability)
            return -logL  #возвращаем отрицательное, так его минимум будет максимумом для logL

        midpoints = [(intervals[i] + intervals[i + 1]) / 2 for i in range(len(frequency))] #начальное приближение
        mean = sum(midpoints[i] * frequency[i] for i in range(len(frequency))) / n
        near_p = 1 / mean

        bounds = [(1e-10, 1 - 1e-10)]

        result = minimize(log_L, near_p, bounds=bounds)

    elif distribution == 'erlang':
        def log_L(t_arr):
            t = float(t_arr[0])
            logL = 0
            for i in range(len(frequency)):
                def erlang_F(x):
                    sum_term = 0
                    for j in range(m):
                        sum_term += (t * x) ** j / math.factorial(j)
                    return 1 - math.exp(-t * x) * sum_term

                F_a = erlang_F(intervals[i])
                F_b = erlang_F(intervals[i + 1])
                probability = max(F_b - F_a, 1e-10)
                logL += frequency[i] * math.log(probability)
            return -logL

        midpoints = [(intervals[i] + intervals[i + 1]) / 2 for i in range(len(frequency))]
        mean = sum(midpoints[i] * frequency[i] for i in range(len(frequency))) / n
        near_t = m / mean

        bounds = [(1e-10, None)]

        result = minimize(log_L, near_t, bounds=bounds)

    return result.x[0]

#Вычисление статистики хи-квадрат для сложной гипотезы
def x_2_statistic(distribution, sample, grouping):
    n = len(sample)
    frequency = []  # частоты встречаемости значения k в интервале
    probability = []  # вероятности попадания в интервал
    k_intervals = 0
    if grouping == 'sturges':
        k_intervals = max(5, int(math.log2(n) + 1))
    elif grouping == 'brooks_carruther':
        k_intervals = max(5, int(5 * math.log(n)))
    elif grouping == 'sqrt':
        k_intervals = max(5, int(math.sqrt(n)))

    if distribution == 'geometric':
        intervals = np.linspace(0, max(sample), k_intervals + 1) #разбиваем примерно на корень н интервалов
        intervals = [math.ceil(x) for x in intervals]

        for i in range(len(intervals) - 1):
            count = 0
            for k in sample:
                if intervals[i] <= k < intervals[i + 1]:
                    count += 1
            frequency.append(count)

        p = omp_grouped_parameter_x('geometric', intervals, frequency)
        points_x[distribution][grouping][n].append(round(float(p),3))

        for i in range(len(intervals) - 1):
            # P(intervals[i] <= k < intervals[i+1]) = F(intervals[i+1]) - F(intervals[i])
            if intervals[i] > 0:
                F_a = 1 - (1 - p) ** intervals[i]
            else:
                F_a = 0
            F_b = 1 - (1 - p) ** intervals[i + 1]
            probability.append(F_b - F_a)

    elif distribution == 'erlang':
        intervals = np.linspace(min(sample), max(sample), k_intervals + 1)

        for i in range(len(intervals) - 1):
            count = 0
            for k in sample:
                if intervals[i] <= k < intervals[i + 1]:
                    count += 1
            frequency.append(count)

        t = omp_grouped_parameter_x('erlang', intervals, frequency)
        points_x[distribution][grouping][n].append(round(float(t),3))

        def erlang_F(x):
            sum_term = 0
            for j in range(m):
                sum_term += (t * x) ** j / math.factorial(j)
            return 1 - math.exp(-t * x) * sum_term

        for i in range(len(intervals) - 1):
            F_a = erlang_F(intervals[i])
            F_b = erlang_F(intervals[i + 1])
            probability.append(F_b - F_a)

    x_square = 0
    for i in range(len(frequency)):
        #ν_i - наблюдаемая частота и np_i - ожидаемая частота
        if (n * probability[i]) > 0:
            x_square += (frequency[i] - n * probability[i]) ** 2 / (n * probability[i])

    N = len(frequency)  #количество интервалов
    s = N - 1 - 1 #степени свободы (-1 так как оцениваем параметр t)

    t_a = chi2.ppf(1 - a, s) #квантиль распределения хи-квадрат

    return x_square, t_a

"""ВЫВОД РЕЗУЛЬТАТОВ"""

with open('../homework_2/sample_generation.json', 'r', encoding='utf-8') as f:
    result = json.load(f)

kolmogorov = {}
x_2 = {}

points_x = {}
points_k = {}

for distribution, data in result.items():
    x_2[distribution] = {}
    points_x[distribution] = {}
    for grouping in ['sturges', 'brooks_carruther', 'sqrt']:
        x_2[distribution][grouping] = {}
        points_x[distribution][grouping] = {}
    for size, samples in data.items():
        for sample in samples:
            if len(sample) not in kolmogorov:
                kolmogorov[len(sample)] = []
                points_k[len(sample)] = []
            for grouping in ['sturges', 'brooks_carruther', 'sqrt']:
                if len(sample) not in x_2[distribution][grouping]:
                    x_2[distribution][grouping][len(sample)] = []
                    points_x[distribution][grouping][len(sample)] = []
                    points_x[distribution][grouping][len(sample)] = []

            """Критерий Колмогорова"""
            if distribution == 'erlang':
                param, P = complex_kolmogorov_test(sample, 1000)
                points_k[len(sample)].append(round(float(param), 3))
                if P < a:
                    kolmogorov[len(sample)].append(
                        f"{round(P, 3)} < {a}, -")
                else:
                    kolmogorov[len(sample)].append(
                        f"{round(P, 3)} >= {a}, +")

            """Критерий хи-квадрат"""
            for grouping in ['sturges', 'brooks_carruther', 'sqrt']:
                x_square, t_a = x_2_statistic(distribution, sample, grouping)

                if x_square >= t_a:
                    x_2[distribution][grouping][len(sample)].append(
                        f"{round(x_square, 3)} >= {round(t_a, 3)}, -")
                else:
                    x_2[distribution][grouping][len(sample)].append(
                        f"{round(x_square, 3)} < {round(t_a, 3)}, +")

def statistic(statist):
    if statist == kolmogorov:
        plus_tests = 0
        for size in statist:
            results = statist[size]
            for r in results:
                if "+" in r:
                    plus_tests += 1
        print(f"erlang: {plus_tests}/{40} ({plus_tests / 40 * 100:.1f}%) прошли тест")
    elif statist == x_2:
        for distribution in ['geometric', 'erlang']:
            plus_tests = 0
            for size in statist[distribution][grouping]:
                results = statist[distribution][grouping][size]
                for r in results:
                    if "+" in r:
                        plus_tests += 1
            print(f"{distribution}: {plus_tests}/{40} ({plus_tests / 40 * 100:.1f}%) прошли тест")

print("КРИТЕРИЙ СОГЛАСИЯ КОЛМОГОРОВА (СМИРНОВА)\nРаспределение Эрланга:\n",kolmogorov)
print("\nСтатистика:")
statistic(kolmogorov)
print("\nОценка параметра t распределения Эрланга:\n",points_k)

print("\nКРИТЕРИЙ СОГЛАСИЯ ХИ_КВАДРАТ")
for grouping in ['sturges', 'brooks_carruther', 'sqrt']:
    print("\n=== Группировка наблюдений: ", grouping, "===")
    for distribution in ['geometric', 'erlang']:
        if distribution == 'geometric':
            print("\nГеометрическое распределение:\n", x_2[distribution][grouping])
        else:
            print("\nРаспределение Эрланга:\n", x_2[distribution][grouping])
            print("\nСтатистика:")
            statistic(x_2)

print("\nОценка параметра p Геометрического распределения:\n",points_x['geometric'])
print("\nОценка параметра t распределения Эрланга:\n",points_x['erlang'])