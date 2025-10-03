import random
import math
import matplotlib.pyplot as plt
import numpy as np

"""Распределение Эрланга"""

def erlang_rand_variable(m, t): # Моделирование случайной величины
    k = 0
    for _ in range(m):
        s = random.random()
        while s == 0:
            s = random.random()
        k += -math.log(s) / t
    return k

# Процедура получения выборки размера n
m = 14
t = 0.125
def erlang_sample(n):
    sample = []
    for i in range(10):
        k = erlang_rand_variable(m, t)
        sample.append(k)
    return sample
print("Выборка из распределения Эрланга:", erlang_sample(10))

# Построение графика
sample = erlang_sample(100)
plt.hist(sample, bins=10, density=True, color='lavender', edgecolor='black', label='Смоделированная выборка')

x_values = np.linspace(0, max(sample), 50)
probability_density = (t**m * x_values**(m-1) * np.exp(-t * x_values)) / math.factorial(m-1) # f(x) = (t^m * x^(m-1) * e^(-t*x)) / (m-1)!
plt.plot(x_values, probability_density, color='violet', linewidth=2, label='Плотность вероятности')

plt.title(f'Распределение Эрланга\n(m={m}, t={t})')
plt.xlabel('Значение случайной величины')
plt.ylabel('Плотность вероятности')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, max(sample))
plt.show()