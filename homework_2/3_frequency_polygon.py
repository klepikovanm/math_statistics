import matplotlib.pyplot as plt
import numpy as np
import math
import json

"""3. Построение гистограммы и полигона частот"""

p = 0.45
m = 14
t = 1 / 8

def frequency_polygon(distribution, size, number):
    with open('sample_generation.json', 'r') as f:
        result = json.load(f)

    sample = result[distribution][str(size)][number - 1]

    bins = 20
    frequencies, intervals = np.histogram(sample, bins=20, density=False) #построение полигона частот
    centers = (intervals[:-1] + intervals[1:]) / 2
    plt.plot(centers, frequencies, 'b-', marker='o', markersize=4, label=f'Полигон')

    if distribution == 'geometric':
        name = 'Геометрическое распределение'
        k_values = np.arange(1, max(sample) + 1)
        distribution_law = []
        for k in k_values:
            probability = p * (1 - p) ** (k - 1)
            distribution_law.append(probability)

        scalability = size * (max(sample) - min(sample)) / bins #масштабирование
        scalability_dist = np.array(distribution_law) * scalability

        plt.plot(k_values, scalability_dist, color='violet', label='Функция вероятности', linewidth=2, alpha=0.8)

    elif distribution == 'erlang':
        name = 'Распределение Эрланга'
        x_values = np.linspace(0, max(sample), 50)
        probability_density = (t ** m * x_values ** (m - 1) * np.exp(-t * x_values)) / math.factorial(m - 1)

        scalability = size * (max(sample) - min(sample)) / bins
        scalability_dist = np.array(probability_density) * scalability

        plt.plot(x_values, scalability_dist, color='violet', label='Плотность распределения')

    plt.title(f'Полигон частот\n{name}, выборка {number}, размер {size}')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
