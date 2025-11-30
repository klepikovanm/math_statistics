import json
import math

"""1. Получение оценок методом моментов и методом максимального правдоподобия"""

p = 0.45
m = 14
t = 1/8

with open('../homework_2/sample_generation.json', 'r', encoding='utf-8') as f:
    result = json.load(f)

geom_points = {}
erlang_points = {}
for distribution, data in result.items():
    for size, samples in data.items():
        for sample in samples:
            if len(sample) not in geom_points:
                geom_points[len(sample)] = []
                erlang_points[len(sample)] = []

            mean = sum(sample) / len(sample)
            geom_point = mean ** (-1)
            erlang_point = geom_point * m
            if distribution == 'geometric':
                geom_points[len(sample)].append(round(geom_point, 5))
            elif distribution == 'erlang':
                erlang_points[len(sample)].append(round(erlang_point, 5))

general_geom = {}
general_erlang = {}
size = [5, 10, 100, 200, 400, 600, 800, 1000]
for i in size:
    if i not in general_geom:
        general_geom[i] = []
        general_erlang[i] = []

    general_geom[i].append(round((sum(geom_points[i]) / 5), 5))
    general_erlang[i].append(round((sum(erlang_points[i]) / 5), 5))

print("ГЕОМЕТРИЧЕСКОЕ РАПРЕДЕЛЕНИЕ\nОМП и ОММ для параметра распределения p:\n",geom_points)
print("Усредненная ОМП и ОММ:\n", general_geom)
print("Истинный параметр: ", p, "\n")

print("РАСПРЕДЕЛЕНИЕ ЭРЛАНГА\nОМП и ОММ для параметра распределения t:\n",erlang_points)
print("Усредненная ОМП и ОММ:\n", general_erlang)
print("Истинный параметр: ", t, "\n")


