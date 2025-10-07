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

print("ГЕОМЕТРИЧЕСКОЕ РАПРЕДЕЛЕНИЕ\nВыборочное среднее:\n",sample_mean["geometric"])
print("Математическое ожидание: ", round((1 / p), 5), "\n")
print("Выборочная дисперсия:\n",sample_variance["geometric"])
print("Дисперсия: ", round(((1 - p) / p**2), 5), "\n\n")

print("РАСПРЕДЕЛЕНИЕ ЭРЛАНГА\nВыборочное среднее:\n",sample_mean["erlang"])
print("Математическое ожидание: ", m / t, "\n")
print("Выборочная дисперсия:\n",sample_variance["erlang"])
print("Дисперсия: ", m / t**2)
