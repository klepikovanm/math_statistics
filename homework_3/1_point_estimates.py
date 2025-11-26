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
                if 'omp' not in erlang_points:
                    erlang_points['omp'] = {}
                    erlang_points['omm'] = {}
                    if 't' not in erlang_points['omp']:
                        erlang_points['omp']['t'] = {}
                        erlang_points['omp']['m'] = {}
                        erlang_points['omm']['t'] = {}
                        erlang_points['omm']['m'] = {}
                erlang_points['omp']['t'][len(sample)] = []
                erlang_points['omp']['m'][len(sample)] = []
                erlang_points['omm']['t'][len(sample)] = []
                erlang_points['omm']['m'][len(sample)] = []

            mean = sum(sample) / len(sample)
            geom_point = mean ** (-1)
            if distribution == 'geometric':
                geom_points[len(sample)].append(round(geom_point, 5))
            elif distribution == 'erlang':
                s = 0
                ln = 0
                for i in sample:
                    s += (i - mean) ** 2
                    ln += math.log(i)

                erlang_omp_t = 1 / (mean * (1 - math.exp(ln / len(sample) - math.log(mean))))
                erlang_omp_m = erlang_omp_t * mean
                erlang_points['omp']['t'][len(sample)].append(round(erlang_omp_t, 5))
                erlang_points['omp']['m'][len(sample)].append(round(erlang_omp_m, 5))

                erlang_omm_t = mean/ (s/len(sample))
                erlang_omm_m = erlang_omm_t * mean
                erlang_points['omm']['t'][len(sample)].append(round(erlang_omm_t, 5))
                erlang_points['omm']['m'][len(sample)].append(round(erlang_omm_m, 5))

general_geom = {}
general_erlang = {}
size = [5, 10, 100, 200, 400, 600, 800, 1000]
for i in size:
    if i not in general_geom:
        general_geom[i] = []
        if 'omp' not in general_erlang:
            general_erlang['omp'] = {}
            general_erlang['omm'] = {}
            if 't' not in general_erlang['omp']:
                general_erlang['omp']['t'] = {}
                general_erlang['omp']['m'] = {}
                general_erlang['omm']['t'] = {}
                general_erlang['omm']['m'] = {}
        general_erlang['omp']['t'][i] = []
        general_erlang['omp']['m'][i] = []
        general_erlang['omm']['t'][i] = []
        general_erlang['omm']['m'][i] = []

    general_geom[i].append(round((sum(geom_points[i]) / 5), 5))
    general_erlang['omp']['t'][i].append(round((sum(erlang_points['omp']['t'][i]) / 5), 5))
    general_erlang['omp']['m'][i].append(round((sum(erlang_points['omp']['m'][i]) / 5), 5))
    general_erlang['omm']['t'][i].append(round((sum(erlang_points['omm']['t'][i]) / 5), 5))
    general_erlang['omm']['m'][i].append(round((sum(erlang_points['omm']['m'][i]) / 5), 5))

print("ГЕОМЕТРИЧЕСКОЕ РАПРЕДЕЛЕНИЕ\nОМП и ОММ для параметра распределения t:\n",geom_points)
print("Усредненная ОМП и ОММ:\n", general_geom)
print("Истинный параметр: ", p, "\n")

print("РАСПРЕДЕЛЕНИЕ ЭРЛАНГА\nОМП для параметра t:\n",erlang_points["omp"]["t"])
print("Усредненная ОМП:\n", general_erlang["omp"]["t"])
print("Истинный параметр: ", t, "\n")
print("ОМП для параметра m:\n",erlang_points["omp"]["m"])
print("Усредненная ОМП:\n", general_erlang["omp"]["m"])
print("Истинный параметр: ", m, "\n")

print("ОММ для параметра t:\n",erlang_points["omm"]["t"])
print("Усредненная ОМП:\n", general_erlang["omm"]["t"])
print("Истинный параметр: ", t, "\n")
print("ОММ для параметра m:\n",erlang_points["omm"]["m"])
print("Усредненная ОМП:\n", general_erlang["omm"]["m"])
print("Истинный параметр: ", m, "\n")


