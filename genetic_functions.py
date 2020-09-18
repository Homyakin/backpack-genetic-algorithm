from typing import List

from models import Backpack, Individual
import random


def create_rand_individual(backpack: Backpack):
    """
    Создает случайную допустимую особь
    :param backpack: Backpack
    :return: list[Individual]
    """
    individual_volume = 0
    available_items = backpack.items
    instance = []
    for _ in backpack.items:
        instance.append(0)  # изначально особь пустая
    while len(available_items) != 0:
        a = []
        for i in available_items:
            if i.volume <= backpack.max_volume - individual_volume:  # смотрим какие предметы еще можем положить
                a.append(i)
        available_items = a
        if len(available_items) == 0:
            continue
        item = random.randint(0, len(available_items) - 1)  # выбираем случайный предмет
        # выбираем случайное количество предмета
        item_count = int(random.randint(1, (backpack.max_volume - individual_volume) // available_items[item].volume))
        if len(available_items) == 1:
            item_count = int((backpack.max_volume - individual_volume) / available_items[item].volume)
        instance[available_items[item].number] += item_count  # добавляем количества предмета на соответствующую позицию
        individual_volume += item_count * available_items[item].volume  # увеличиваем текущую вместимость особи
    return Individual(instance, count_individual_cost(instance, backpack))


def create_start_generation(backpack: Backpack):
    """
    Создает стартовое поколение
    :param backpack: Backpack
    :return: стартовое поколение list[Individual]
    """
    generation = []
    for i in range(backpack.max_individuals):
        generation.append(create_rand_individual(backpack))
    return generation


def count_individual_cost(instance: list, backpack: Backpack):
    cost = 0
    for i in range(len(instance)):
        cost += instance[i] * backpack.items[i].cost
    return cost


def check_instance_volume(instance: List[int], backpack: Backpack):
    volume = 0
    for i in range(len(instance)):
        volume += instance[i] * backpack.items[i].volume
    return volume <= backpack.max_volume


def rand_crossover(parent_1: Individual, parent_2: Individual, backpack: Backpack):
    new_instance = []

    for _ in range(10):
        for i in range(len(parent_1.items)):
            parent = random.randint(1, 2)
            new_instance.append(parent_1.items[i] if parent == 1 else parent_2.items[i])

        if check_instance_volume(new_instance, backpack):
            # print("ОНО РАБОТАЕТ")
            return Individual(new_instance, count_individual_cost(new_instance, backpack))
        new_instance = []

    return parent_1 if parent_1.cost > parent_2.cost else parent_2


def clever_crossover(parent_1: Individual, parent_2: Individual, backpack: Backpack):
    new_instance = []

    for i in range(len(parent_1.items)):
        s = parent_1.items[i] + parent_2.items[i]
        new_instance.append(s // 2)

    return Individual(new_instance, count_individual_cost(new_instance, backpack))


def crossover(parent_1: Individual, parent_2: Individual, backpack: Backpack):
    return rand_crossover(parent_1, parent_2, backpack)


def mutation(backpack: Backpack):
    return create_rand_individual(backpack)


def create_new_generation(backpack: Backpack, generation: List[Individual]):
    new_generations = []

    for i in range(2 * backpack.max_individuals):
        mutation_probability = random.randint(1, 100)
        if mutation_probability <= backpack.mutation_probability:
            new_generations.append(mutation(backpack))
            continue
        parent_1 = generation[random.randint(0, len(generation) - 1)]
        parent_2 = generation[random.randint(0, len(generation) - 1)]
        crossover_probability = random.randint(1, 100)
        if crossover_probability <= backpack.crossover_probability:
            new_generations.append(crossover(parent_1, parent_2, backpack))
            continue
        new_generations.append(parent_1 if parent_1.cost > parent_2.cost else parent_2)
    generation = sorted(generation, key=lambda x: x.cost, reverse=True)
    for i in range(backpack.alpha):
        new_generations.append(generation[i])
    new_generations = sorted(new_generations, key=lambda x: x.cost, reverse=True)

    return new_generations[0:backpack.max_individuals]
