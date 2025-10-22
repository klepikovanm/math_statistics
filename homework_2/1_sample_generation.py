import random
import math
import json

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
    for i in range(n):
        k = erlang_rand_variable(m, t)
        sample.append(k)
    return sample

"""1. Генерация выборок выбранных случайных величин"""

# Генерация выборок
size = [5, 10, 100, 200, 400, 600, 800, 1000]
geometric_result = {}
erlang_result = {}

max_geometric = [geometric_sample(1000) for _ in range(5)]
max_erlang = [erlang_sample(1000) for _ in range(5)]

for i in size:
    if i not in geometric_result:
        geometric_result[i] = []
        erlang_result[i] = []
    for j in range(5):
        geometric_result[i].append(max_geometric[j][:i])
        erlang_result[i].append(max_erlang[j][:i])

# Запись в файл
result = {
    "geometric": geometric_result,
    "erlang": erlang_result
}
with open('sample_generation.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4)
