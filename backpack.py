import random


class Backpack:
    def __init__(self, types_count):
        self.volumes = []  # объемы вещей
        self.costs = []  # стоимости вещей
        self.max_volume = random.randint(20, 200)  # максимальный объем рюкзака
        self.alpha = 2  # количество лучших особей из предыдущего поколения
        self.epsilon = 0.05  # точность функции приспособленности
        self.max_generations = random.randint(500, 1000)  # максимальное количество поколений
        self.crossover_probability = random.randint(85, 99)  # вероятность кроссовера
        self.mutation_probability = random.randint(3, 6)  # вероятность мутации


class Individual:
    def __init__(self, items: list, cost: int):
        self.items = items
        self.cost = cost
