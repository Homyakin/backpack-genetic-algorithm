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
