import random
from models import Backpack, Item
from genetic_functions import create_start_generation

print("Задайте количество различных типов предметов")
types_count = int(input())

print("Выберите способ задания начальных условий:")
print("1. Ручной")
print("2. Случайный")

case = input()

backpack = Backpack(types_count)

if case == "2":
    items = []
    for i in range(types_count):
        item = Item(i, random.randint(1, 20), random.randint(1, 20))
        items.append(item)
    backpack.items = items
    print("Список предметов:", backpack.items)
    print("Максимальная вместимость:", backpack.max_volume)
    print("Количество лучших особей из предыдущего поколения:", backpack.alpha)
    print("Точность функции приспособленности:", backpack.epsilon)
    print("Максимальное количество поколений:", backpack.max_generations)
    print("Максимальное количество особей в поколении:", backpack.max_individuals)
    print("Вероятность кроссовера: ", backpack.crossover_probability, "%", sep='')
    print("Вероятность мутации: ", backpack.mutation_probability, "%", sep='')

print(create_start_generation(backpack))
