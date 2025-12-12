import json
import numpy as np
import math
from scipy.stats import chi2

"""1. Проверка гипотезы о виде распределения"""

p = 0.45
m = 14
t = 1/8

a = 0.05
lambda_a = 1.36

def kolmogorov_statistic(sample):
    n = len(sample)
    D_plus = 0
    D_minus = 0
    sorted_sample = sorted(sample)

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
    s = N - 1 #степени свободы

    t_a = chi2.ppf(1 - a, s) #квантиль распределения хи-квадрат

    return x_square, t_a

with open('../homework_2/sample_generation.json', 'r', encoding='utf-8') as f:
    result = json.load(f)

kolmogorov = {}
x_2 = {}
for distribution, data in result.items():
    x_2[distribution] = {}
    for grouping in ['sturges', 'brooks_carruther', 'sqrt']:
        x_2[distribution][grouping] = {}
    for size, samples in data.items():
        for sample in samples:
            if len(sample) not in kolmogorov:
                kolmogorov[len(sample)] = []
            for grouping in ['sturges', 'brooks_carruther', 'sqrt']:
                if len(sample) not in x_2[distribution][grouping]:
                    x_2[distribution][grouping][len(sample)] = []

            """Критерий Колмогорова"""
            if distribution == 'erlang':
                D = kolmogorov_statistic(sample)

                if len(sample) >= 20:
                    if (math.sqrt(len(sample)) * D >= lambda_a):
                        kolmogorov[len(sample)].append(
                            f"{round(math.sqrt(len(sample)) * D, 3)} >= {lambda_a}, -")
                    else:
                        kolmogorov[len(sample)].append(
                            f"{round(math.sqrt(len(sample)) * D, 3)} < {lambda_a}, +")
                else:
                    if ((6 * len(sample) * D + 1) / (6 * math.sqrt(len(sample))) >= lambda_a):
                        kolmogorov[len(sample)].append(
                            f"{round((6 * len(sample) * D + 1) / (6 * math.sqrt(len(sample))), 3)} >= {lambda_a}, -")
                    else:
                        kolmogorov[len(sample)].append(
                            f"{round((6 * len(sample) * D + 1) / (6 * math.sqrt(len(sample))), 3)} < {lambda_a}, +")

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
