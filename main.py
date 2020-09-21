import random
from os import system, name

from models import BackpackFactory, Item


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


clear()

print("Выберите способ задания начальных условий:")
print("1. Ручной")
print("2. Случайный")
print("3. Тест кейс 1")
print("4. Тест кейс 2")


case = input()


def input_items(n_items):
    items = []
    for i in range(n_items):
        volume = int(input(f"Введите объем вещи {i}: "))
        cost = int(input(f"Введите стоимость вещи {i}: "))
        items.append(Item(i, volume, cost))
    return items


if case in ("1", "2"):
    types_count = int(input("Задайте количество различных типов предметов: "))

if case == "1":
    max_volume = int(input("Введите объем рюкзака: "))
    alpha = int(input("Введите количество лучших особей из предыдущего поколения, которые будут в следующем: "))
    max_generations = int(input("Введите максимальное количество поколений: "))
    max_specimen = int(input("Введите максимальное количество особей в поколении: "))
    crossover_type = input("Введите тип кроссовера (random, avg): ")
    crossover_probability = float(input("Введите вероятность кроссовера: "))
    mutation_probability = float(input("Введите вероятность мутации: "))
    epsilon = float(input("Введите точность функции приспособленности: "))

    items = input_items(types_count)
    backpack = BackpackFactory(items, 
                               max_volume, 
                               alpha, 
                               max_generations, 
                               max_specimen, 
                               crossover_type, 
                               crossover_probability, 
                               mutation_probability, 
                               epsilon)

elif case == "2":
    items = [Item(i, random.randint(1, 20), random.randint(1, 20)) for i in range(types_count)]
    backpack = BackpackFactory(items)
elif case == "3":
    print("Объем рюкзака: 58",
          "Оптимальное решение:",
          "\t1 - 2шт, 2 - 1шт, 3 - 2шт.",
          "Запуск алгоритма:",
          sep="\n",
          end="\n")

    items = [Item(0, 7, 12),
             Item(1, 3, 2),
             Item(2, 20, 41)]
    backpack = BackpackFactory(items,
                               max_volume=58)

elif case == "4":
    print("Объем рюкзака: 45",
          "Оптимальное решение:",
          "\t1 - 0шт, 2 - 0шт, 3 - 3шт.",
          "Запуск алгоритма:",
          sep="\n",
          end="\n")

    items = [Item(0, 12, 40),
             Item(1, 20, 60),
             Item(2, 15, 50)]
    backpack = BackpackFactory(items,
                               max_volume=45)
else:
    exit(1)

print("Список предметов: ")
for item in backpack.items:
    print(item)
print()

print("Максимальная вместимость: ", backpack.max_volume)
print("Количество лучших особей из предыдущего поколения: ", backpack.alpha)
print("Точность функции приспособленности: ", backpack.epsilon)
print("Максимальное количество поколений: ", backpack.max_generations)
print("Максимальное количество особей в поколении: ", backpack.max_specimen)
print("Вероятность кроссовера: ", backpack.crossover_probability)
print("Вероятность мутации: ", backpack.mutation_probability)

backpack.evolve()
