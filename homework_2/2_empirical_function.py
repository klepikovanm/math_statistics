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

    sample = result[distribution][str(size)][number-1]
    dist = []
    if distribution == 'geometric':
        name = 'Геометрическое распределение'
        k_values = np.arange(1, max(sample) + 1)
        distribution_law = []
        for k in k_values:
            F = 1 - (1 - p) ** k # P(X ≤ k) = 1 - ( 1 - p)^k
            distribution_law.append(F)
        dist.append(k_values)
        dist.append(distribution_law)
    elif distribution == 'erlang':
        name = 'Распределение Эрланга'
        x_values = np.linspace(0, max(sample), 50)
        probability = []
        for x in x_values:
            sum_term = 0
            for k in range(m):
                sum_term += (t * x) ** k / math.factorial(k)
            F = 1 - math.exp(-t * x) * sum_term # F = 1 - e^(-t*x) * Σ[(t*x)^k / k!] для k=0 до m-1
            probability.append(F)
        dist.append(x_values)
        dist.append(probability)
    sorted_sample = np.sort(sample)
    F = np.arange(1, size + 1) / size

    return [sorted_sample, F, name, dist]

def separate_graph(distribution, size, number): # Функция для построения отдельных графиков
    data = empirical_func(distribution, size, number)

    plt.step(data[0], data[1], color='blue', where='post', label='ЭФР')
    plt.plot(data[3][0], data[3][1], color='violet', label='Теоретическая ФР')

    plt.title(f'Эмпирическая функция распределения\n{data[2]}, выборка {number}, размер {size}')
    plt.xlabel('t')
    plt.ylabel('Fn(t)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1.1)
    plt.show()

def all_graphs(distribution, size): # Функция для построения графиков для всех выборок распределения одного размера
    colors = ['red', 'blue', 'black', 'green', 'orange']
    for i in range(5):
        data = empirical_func(distribution, size, i)
        plt.step(data[0], data[1], color=colors[i], where='post', label=f'ЭФР {i+1}')
        name = data[2]
        dist_func = data[3]
    plt.plot(dist_func[0], dist_func[1], color='violet', label='Теоретическая ФР')

    plt.title(f'Эмпирическая функция распределения\n{name}, размер {size}')
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
