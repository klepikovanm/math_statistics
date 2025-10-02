import random
import math

"""Геометрическое распределение"""

def geometric_rand_variable(p): # Моделирование случайной величины
    s = random.random()
    k = 0
    distribution_func = p  #Fs(X)=P(s<=X)
    while s > distribution_func:
        k += 1
        distribution_func = 1 - (1 - p)**(k + 1)
    return k

# Процедура получения выборки размера 10
p = 0.45
geometric_sample = []
for i in range(10):
    k = geometric_rand_variable(p)
    geometric_sample.append(k)

print("Выборка из геометрического распределения:", geometric_sample)

"""Распределение Эрланга"""

def erlang_rand_variable(m, t): # Моделирование случайной величины
    k = 0
    for _ in range(m):
        s = random.random()
        while s == 0:
            s = random.random()
        k += -math.log(s) / t
    return k

# Процедура получения выборки размера 10
m = 14
t = 0.125
erlang_sample = []
for i in range(10):
    k = erlang_rand_variable(m, t)
    erlang_sample.append(k)
print("Выборка из распределения Эрланга:", erlang_sample)