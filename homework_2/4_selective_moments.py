import json

"""4. Вычисление выборочных моментов"""

p = 0.45
m = 14
t = 1/8

with open('sample_generation.json', 'r', encoding='utf-8') as f:
    result = json.load(f)

sample_mean = {}
sample_variance = {}
for distribution, data in result.items():
    sample_mean[distribution] = {}
    sample_variance[distribution] = {}
    for size, samples in data.items():
        for sample in samples:
            if len(sample) not in sample_mean[distribution]:
                sample_mean[distribution][len(sample)] = []
                sample_variance[distribution][len(sample)] = []
            mean = sum(sample) / len(sample)
            sample_mean[distribution][len(sample)].append(round(mean, 5))
            s = 0
            for i in sample:
                s += (i - mean) ** 2
            sample_variance[distribution][len(sample)].append(round(s / len(sample), 5))

general_mean = {}
general_variance = {}
for distribution, data in result.items():
    general_mean[distribution] = {}
    general_variance[distribution] = {}
    size = [5, 10, 100, 200, 400, 600, 800, 1000]
    for i in size:
        if i not in general_mean[distribution]:
            general_mean[distribution][i] = []
            general_variance[distribution][i] = []
        general_mean[distribution][i].append(round((sum(sample_mean[distribution][i]) / 5), 5))
        general_variance[distribution][i].append(round((sum(sample_variance[distribution][i]) / 5), 5))


print("ГЕОМЕТРИЧЕСКОЕ РАПРЕДЕЛЕНИЕ\nВыборочное среднее для всех выборок:\n",sample_mean["geometric"])
print("Усредненное выборочное среднее:\n", general_mean["geometric"])
print("Математическое ожидание: ", round((1 / p), 5), "\n")
print("Выборочная дисперсия для всех выборок:\n",sample_variance["geometric"])
print("Усредненная выборочная дисперсия:\n", general_variance["geometric"])
print("Дисперсия: ", round(((1 - p) / p**2), 5), "\n\n")

print("РАСПРЕДЕЛЕНИЕ ЭРЛАНГА\nВыборочное среднее для всех выборок:\n",sample_mean["erlang"])
print("Усредненное выборочное среднее:\n", general_mean["erlang"])
print("Математическое ожидание: ", m / t, "\n")
print("Выборочная дисперсия для всех выборок:\n",sample_variance["erlang"])
print("Усредненная выборочная дисперсия:\n", general_variance["erlang"])
print("Дисперсия: ", m / t**2)
