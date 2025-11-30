import json
import math
import matplotlib.pyplot as plt
import numpy as np

"""2. Построение эмпирической функции распределения"""

p = 0.45
m = 14
t = 1/8

def empirical_func(distribution, size, number): # Поиск значний для создания графика
    with open('sample_generation.json', 'r') as f:
        result = json.load(f)

    sample = result[distribution][str(size)][number]
    dist = []
    if distribution == 'geometric':
        name = 'Геометрическое распределение'
        max_k = max(max(result[distribution][str(size)][j]) for j in range(5))
        k_values = np.arange(1, max_k + 1)
        distribution_law = []
        for k in k_values:
            F = 1 - (1 - p) ** k # P(X ≤ k) = 1 - ( 1 - p)^k
            distribution_law.append(F)
        dist.append(k_values)
        dist.append(distribution_law)
    elif distribution == 'erlang':
        name = 'Распределение Эрланга'
        x_values = np.linspace(0, max(sample), 50)
        distribution_law = []
        for x in x_values:
            sum_term = 0
            for k in range(m):
                sum_term += (t * x) ** k / math.factorial(k)
            F = 1 - math.exp(-t * x) * sum_term # F = 1 - e^(-t*x) * Σ[(t*x)^k / k!] для k=0 до m-1
            distribution_law.append(F)
        dist.append(x_values)
        dist.append(distribution_law)
    sorted_sample = np.sort(sample)
    F = np.arange(1, size + 1) / size

    return [sorted_sample, F, name, dist]

def separate_graph(distribution, size): # Функция для построения отдельного графика
    all_data = []
    for i in range(5):
        all_data.append(empirical_func(distribution, size, i))

    general_F = []
    for i in range(size):
        general_F.append(sum(data[1][i] for data in all_data) / 5)

    x_values = all_data[0][3][0]
    probability = np.mean([data[3][1] for data in all_data], axis=0)

    plt.step(all_data[0][0], general_F, color='blue', where='post', label='ЭФР')
    plt.plot(x_values, probability, color='violet', label='Теоретическая ФР')

    plt.title(f'Эмпирическая функция распределения\n{all_data[0][2]}, размер {size}')
    plt.xlabel('t')
    plt.ylabel('Fn(t)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1.1)
    plt.show()

def all_graphs(distribution): # Функция для построения общего графика для всех размеров выборок
    size = [5, 10, 100, 200, 400, 600, 800, 1000]
    colors = ['red', 'blue', 'black', 'green', 'orange', 'grey', 'purple', 'lime']

    for i in range(len(size)):
        all_data = []
        for j in range(5):
            data = empirical_func(distribution, size[i], j)
            all_data.append(data)
            name = data[2]
            dist_func = data[3]

        general_F = []
        for k in range(size[i]):
            general_F.append(sum(data[1][k] for data in all_data) / 5)

        plt.step(all_data[0][0], general_F, color=colors[i], where='post', label=f'ЭФР размер {size[i]}')

    plt.plot(dist_func[0], dist_func[1], color='violet', label='Теоретическая ФР')

    plt.title(f'Эмпирическая функция распределения\n{name}')
    plt.xlabel('t')
    plt.ylabel('Fn(t)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1.1)
    plt.show()

"""Вычисление Dm,n"""

def calculation_D(distribution, size_m, size_n, number_m, number_n):
    F_m = empirical_func(distribution, size_m, number_m)
    F_n = empirical_func(distribution, size_n, number_n)

    all_values = [] #объединяем точки из двух функций
    all_values.extend(F_n[0])
    all_values.extend(F_m[0])
    all_values = sorted(set(all_values))

    max_sup = 0
    for value in all_values: #ищем значения в каждой точкке для каждой функции
        value_n = 0
        for i in range(len(F_n[0])):
            x = F_n[0][i]  #точка скачка - ось х
            if x <= value:
                value_n = F_n[1][i]  #значение ЭФР - ось у
            else:
                break
        value_m = 0
        for i in range(len(F_m[0])):
            x = F_m[0][i]
            if x <= value:
                value_m = F_m[1][i]
            else:
                break

        sup = abs(value_n - value_m)
        if sup > max_sup:
            max_sup = sup

    D = np.sqrt((size_n * size_m) / (size_n + size_m)) * max_sup
    D = round(D, 6)
    return D


def calculation_general_D(distribution, size_m, size_n):
    all_D = []
    for number_m in range(5):
        for number_n in range(5):
            D_value = calculation_D(distribution, size_m, size_n, number_m, number_n)
            all_D.append(D_value)

    general_D = sum(all_D) / len(all_D)

    return round(general_D, 5)

print(calculation_general_D('erlang',800,1000))
