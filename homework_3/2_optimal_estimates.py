import json

"""2. Поиск оптимальных оценок"""

p = 0.45
m = 14
t = 1/8

with open('../homework_2/sample_generation.json', 'r', encoding='utf-8') as f:
    result = json.load(f)

estimates = {}
for distribution, data in result.items():
    estimates[distribution] = {}
    for size, samples in data.items():
        for sample in samples:
            if len(sample) not in estimates[distribution]:
                estimates[distribution][len(sample)] = []
            mean = sum(sample) / len(sample)
            if distribution == 'geometric':
                estimates[distribution][len(sample)].append(round(mean, 5))
            elif distribution == 'erlang':
                estimate = mean / m
                estimates[distribution][len(sample)].append(round(estimate, 5))

general_estimates = {}
for distribution, data in result.items():
    general_estimates[distribution] = {}
    size = [5, 10, 100, 200, 400, 600, 800, 1000]
    for i in size:
        if i not in general_estimates[distribution]:
            general_estimates[distribution][i] = []
        general_estimates[distribution][i].append(round((sum(estimates[distribution][i]) / 5), 5))

print(f"ГЕОМЕТРИЧЕСКОЕ РАПРЕДЕЛЕНИЕ\nОптимальная оценка для параметрической функции 1/p = {round(1/p,5)}:\n",estimates["geometric"])
print("Усредненная оптимальная оценка:\n", general_estimates["geometric"])

print(f"\nРАСПРЕДЕЛЕНИЕ ЭРЛАНГА\nОптимальная оценка для параметрической функции 1/t = {1/t}:\n",estimates["erlang"])
print("Усредненная оптимальная оценка:\n", general_estimates["erlang"])

