from backpack import Backpack


def create_rand_individual(backpack: Backpack):
    """
    Создает случайную допустимую особь
    :param backpack: Backpack
    :return: list[Individual]
    """
    individual_volume = 0
    available_items = backpack.volumes
    while len(available_items) != 0:
        a = []
        for i in available_items:
            if i <= backpack.max_volume - individual_volume:
                a.append(i)
        available_items = a
    pass


def create_start_generation(backpack: Backpack):
    """
    Создает стартовое поколение
    :param backpack: Backpack
    :return: стартовое поколение list[Individual]
    """
    generation = []
    for i in range(backpack.max_generations):
        generation.append(create_rand_individual(backpack))
    return generation
