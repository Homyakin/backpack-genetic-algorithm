import random


class Backpack:
    def __init__(self, types_count):
        self.types_count = types_count
        self.items = []  # предметы (Item)
        self.max_volume = random.randint(50, 300)  # максимальный объем рюкзака
        self.alpha = 2  # количество лучших особей из предыдущего поколения
        self.epsilon = 0.05  # точность функции приспособленности
        self.max_generations = random.randint(1000, 3000)  # максимальное количество поколений
        self.max_individuals = random.randint(500, 2000)  # максимальное количество особей в поколении
        self.crossover_probability = random.randint(85, 99)  # вероятность кроссовера
        self.mutation_probability = random.randint(3, 6)  # вероятность мутации


class Individual:
    def __init__(self, items: list, cost: int):
        self.items = items
        self.cost = cost

    def __repr__(self):
        return "[Стоимость {}; веса: {}]".format(self.cost, self.items)


class Item:
    def __init__(self, number: int, volume: int, cost: int):
        self.number = number
        self.volume = volume
        self.cost = cost

    def __repr__(self):
        return "[Вес: {}. Стоимость: {}]".format(self.volume, self.cost)
