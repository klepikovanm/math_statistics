import random
import matplotlib.pyplot as plt
import numpy as np

"""Геометрическое распределение"""

def geometric_rand_variable(p): # Моделирование случайной величины
    s = random.random()
    k = 1
    distribution_func = p  #Fs(X)=P(s<=X)
    while s > distribution_func:
        k += 1
        distribution_func = 1 - (1 - p)**k
    return k

# Процедура получения выборки размера n
p = 0.45
def geometric_sample(n):
    sample = []
    for i in range(n):
        k = geometric_rand_variable(p)
        sample.append(k)
    return sample
print("Выборка из геометрического распределения:", geometric_sample(10))

# Построение графика
sample = geometric_sample(100)
plt.hist(sample, bins=range(1, max(sample) + 2), density=True, color='lavender', edgecolor='black', label='Смоделированная выборка')

k_values = np.arange(1, max(sample) + 1)
distribution_law = []
for k in k_values:
    probability = p * (1 - p) ** (k - 1) #P(X=k) = p * (1-p)^(k-1)
    distribution_law.append(probability)
plt.plot(k_values, distribution_law, 'o-', color='violet', linewidth=2, markersize=4, label='Закон распределения')

plt.title(f'Геометрическое распределение\n(p={p})')
plt.xlabel('Значение случайной величины')
plt.ylabel('Вероятность')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
