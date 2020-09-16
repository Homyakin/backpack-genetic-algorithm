import random

from backpack import Backpack

print("Задайте количество различных типов предметов")
types_count = int(input())

print("Выберите способ задания начальных условий:")
print("1. Ручной")
print("2. Случайный")

case = input()

backpack = Backpack(types_count)

if case == "2":
    volumes = []
    costs = []
    for i in range(types_count):
        volumes.append(random.randint(1, 20))
        costs.append(random.randint(1, 20))
    backpack.volumes = volumes
    backpack.costs = costs
    print("Веса предметов:", backpack.volumes)
    print("Стоимости предметов:", backpack.costs)
    print("Максимальная вместимость:", backpack.max_volume)
    print("Количество лучших особей из предыдущего поколения:", backpack.alpha)
    print("Точность функции приспособленности:", backpack.epsilon)
    print("Максимальное количество поколений:", backpack.max_generations)
    print("Вероятность кроссовера: ", backpack.crossover_probability, "%", sep='')
    print("Вероятность мутации: ", backpack.mutation_probability, "%", sep='')
