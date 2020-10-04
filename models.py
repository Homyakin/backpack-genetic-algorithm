import random
from copy import deepcopy


class BackpackFactoryParallelLauncher:
    """
    Завод по параллельному укладыванию вещей в рюкзаки.

    :param items: Предметы
    :param max_volume: Максимальный объем рюкзака
    :param n_populations: Количество параллельно развивающихся популяций
    :param populations_params: Параметры популяций (если None, то берутся случайные)
    :param migration_delay: Количество поколений перед миграцией
    :param migration_proba: Вероятность миграции
    :param n_migrations: Максимальное кол-во миграций
    :param epsilon: Точность функции приспособленности
    """

    def __init__(self,
                 items,
                 max_volume=50,
                 n_populations=10,
                 populations_params=None,
                 migration_delay=25,
                 migration_proba=.1,
                 n_migrations=100,
                 epsilon=.001):
        self.items = items
        self.max_volume = max_volume
        self.n_populations = n_populations
        if populations_params is not None:
            assert len(
                populations_params) == n_populations, "len of populations_params don't match with n_populations"
            self.populations_params = populations_params
        else:
            self.populations_params = [
                self.generate_random_params() for _ in range(n_populations)]

        self.migration_delay = migration_delay
        self.migration_proba = migration_proba
        self.n_migrations = n_migrations
        self.epsilon = epsilon

    def generate_random_params(self):
        max_specimen = random.randint(25, 1000)
        alpha = random.randint(0, max_specimen // 2)
        crossover_type = "avg" if random.randint(0, 1) == 0 else "rand"
        crossover_probability = 1 - random.random() / 2
        mutation_probability = random.random() / 4

        return {"alpha": alpha,
                "max_specimen": max_specimen,
                "crossover_type": crossover_type,
                "crossover_probability": crossover_probability,
                "mutation_probability": mutation_probability}

    def init_populations(self):
        populations = []
        for params in self.populations_params:
            slave = BackpackFactory(
                items=self.items,
                max_volume=self.max_volume,
                alpha=params["alpha"],
                max_specimen=params["max_specimen"],
                crossover_type=params["crossover_type"],
                crossover_probability=params["crossover_probability"],
                mutation_probability=params["mutation_probability"],
                epsilon=self.epsilon
            )

            populations.append(slave)

        self.populations = populations

    def migrate(self):
        for population_number, population in enumerate(self.populations):
            for backpack_number, backpack in enumerate(
                    population.cur_generation):
                if random.random() < self.migration_proba:
                    r = [
                        number for number in range(
                            self.n_populations) if number != population_number]
                    target_population = random.choice(r)
                    self.populations[target_population].cur_generation.append(
                        backpack)
                    self.populations[population_number].cur_generation.pop(
                        backpack_number)

    def evolve(self):
        self.init_populations()
        def func(x): return x.evolve(max_generations=self.migration_delay)
        avg_fitness = 0
        for i in range(self.n_migrations):
            list(map(func, self.populations))
            self.migrate()
            print(
                f"Миграция {i+1}, прошло поколений: {(i+1) * self.migration_delay}")
            new_avg_fitness = sum(population.cur_generation.cost
                                  for population in self.populations) / self.n_populations
            print(
                f"Среднее значение функции приспособленности: {new_avg_fitness}")
            self.populations[0].get_info()
            if abs(new_avg_fitness - avg_fitness) < self.epsilon:
                break
            avg_fitness = new_avg_fitness
        print("В конце")
        print(f"Среднее значение функции приспособленности: {new_avg_fitness}")
        self.populations[0].get_info()


class BackpackFactory:
    """
    Завод по укладыванию вещей в рюкзаки.

    :param items: Предметы
    :param max_volume: Максимальный объем рюкзака
    :param alpha: Количество лучших особей из предыдущего поколения,
        которые пойдут в следующее
    :param max_generations: Максимальное количество поколений
    :param max_specimen: Максимальное количество особей в поколении
    :param crossover_type: Тип кроссовера.
        Rand -- случайный выбор
        Avg -- среднее между родителями
    :param crossover_probability: Вероятность кроссовера
    :param mutation_probability: Вероятность мутации
    :param epsilon: Точность функции приспособленности
    """

    def __init__(self,
                 items,
                 max_volume=50,
                 alpha=2,
                 max_generations=5000,
                 max_specimen=100,
                 crossover_type="avg",
                 crossover_probability=.85,
                 mutation_probability=.1,
                 epsilon=.001):

        assert crossover_type in ("rand", "avg"), "Invalid crossover type"

        self.items = items  # List of Item
        self.types_count = len(items)
        self.max_volume = max_volume
        self.alpha = alpha
        self.max_generations = max_generations
        self.max_specimen = max_specimen
        if crossover_type == "rand":
            self.crossover = self.rand_crossover
        else:
            self.crossover = self.avg_crossover
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.epsilon = epsilon

        self.cur_generation = None
        self.epochs_evolved = 0

    def create_rand_backpack(self):
        """Создает случайную допустимую особь."""

        backpack_volume = 0
        available_items = self.items
        item_counts = [0] * self.types_count  # изначально особь пустая
        while len(available_items) != 0:
            available_items = list(
                filter(
                    lambda x: x.volume <= self.max_volume -
                    backpack_volume,
                    available_items))
            if len(available_items) == 0:
                break
            item = random.choice(available_items)  # выбираем случайный предмет

            # выбираем случайное количество предмета
            if len(available_items) == 1:
                item_count = int(
                    (self.max_volume - backpack_volume) / item.volume)
            else:
                item_count = random.randint(
                    1, (self.max_volume - backpack_volume) // item.volume)

            # добавляем количества предмета на соответствующую позицию
            item_counts[item.number] += item_count
            # увеличиваем текущую вместимость особи
            backpack_volume += item_count * item.volume

        return Backpack(self.items, item_counts)

    def create_start_generation(self):
        """Создает стартовое поколение."""

        backpacks = [self.create_rand_backpack()
                     for _ in range(self.max_specimen)]
        return Generation(backpacks)

    def rand_crossover(self, parent_1, parent_2):
        """Проводит случайный кроссовер (случайный выбор частей родителей)."""

        for _ in range(10):  # TODO: чекнуть кол-во попыток

            crossover_counts = [random.choice([par1_arg, par2_arg])
                                for par1_arg, par2_arg in zip(parent_1.item_counts,
                                                              parent_2.item_counts)]
            backpack = Backpack(self.items, crossover_counts)
            if backpack.volume <= self.max_volume:
                return backpack

        return parent_1 if parent_1.cost > parent_2.cost else parent_2

    def avg_crossover(self, parent_1, parent_2):
        """Проводит avg кроссовер (Среднее частей родителей)."""
        for _ in range(10):  # TODO: чекнуть кол-во попыток
            crossover_counts = [
                (par1_arg + par2_arg) // 2 for par1_arg,
                par2_arg in zip(
                    parent_1.item_counts,
                    parent_2.item_counts)]
            backpack = Backpack(self.items, crossover_counts)
            if backpack.volume <= self.max_volume:
                return backpack
        return parent_1 if parent_1.cost > parent_2.cost else parent_2

    def create_new_generation(self, generation):
        """Создает новое поколение особей."""
        new_backpacks = []

        for _ in range(2 * self.max_specimen):
            if random.random() <= self.mutation_probability:
                mutated_backpack = self.create_rand_backpack()
                new_backpacks.append(mutated_backpack)
                continue

            parent_1, parent_2 = random.sample(list(generation), k=2)

            if random.random() <= self.crossover_probability:
                crossovered_backpack = self.crossover(parent_1, parent_2)
                new_backpacks.append(crossovered_backpack)
                continue

            new_backpacks.append(
                parent_1 if parent_1.cost > parent_2.cost else parent_2)

        alpha_best = sorted(
            generation,
            key=lambda x: x.cost,
            reverse=True)[
            :self.alpha]
        new_backpacks.extend(alpha_best)
        new_backpacks = sorted(
            new_backpacks,
            key=lambda x: x.cost,
            reverse=True)

        return Generation(new_backpacks[0:self.max_specimen])

    def get_info(self):
        if self.cur_generation is None:
            return
        print(f"Прошло поколений {self.epochs_evolved}")
        print(
            f"Приспособленность текущего поколения {self.cur_generation.cost:.4f}")
        print(
            f"Лучшая особь: {sorted(self.cur_generation, key=lambda x: x.cost)[0]}\n")

    def evolve(self, max_generations=None, verbose=False):
        """Запускает процесс эволюции."""

        max_generations = max_generations or self.max_generations
        if self.cur_generation is None:
            generation = self.create_start_generation()
        else:
            generation = self.cur_generation

        max_cost = generation.cost

        for i in range(1, max_generations + 1):
            self.epochs_evolved += 1
            new_generation = self.create_new_generation(generation)
            new_cost = new_generation.cost

            if i % 10 == 0:
                if verbose:
                    print(
                        f"Приспособленность поколения {i}: {generation.cost:.4f}")

            if abs(new_generation.cost - generation.cost) < self.epsilon:
                if verbose:
                    print(f"Поколение {i} -- выход")
                break

            if new_cost > max_cost:
                max_cost = new_cost

            generation = new_generation
            self.cur_generation = generation

        if verbose:
            self.get_info()
            print(f"Максимальное значение приспособленности: {max_cost:.4f}")
        return generation


class Generation:
    """
    Поколение особей.

    :param backpacks: Список особей
    """

    def __init__(self, backpacks):
        self.backpacks = backpacks

    @property
    def cost(self):
        return sum(item.cost for item in self) / len(self)

    def append(self, item):
        self.backpacks.append(item)

    def pop(self, key):
        item = self.backpacks[key]
        del self.backpacks[key]
        return item

    def __len__(self):
        return len(self.backpacks)

    def __getitem__(self, key):
        return self.backpacks[key]

    def __delitem__(self, key):
        del self.backpacks[key]

    def __iter__(self):
        return iter(self.backpacks)

    def __repr__(self):
        objs = "\n".join(backpack.__repr__() for backpack in self)
        cost = self.cost
        return f'''Объекты: {objs}\nПриспособленность поколения: {cost}\n'''


class Backpack:
    """
    Рюкзак.

    :param items: Список всех вещей
    :param item_counts: Список из количеств каждой вещи, лежащих в рюкзаке
    """

    def __init__(self, items, item_counts):
        self.items = items
        self.item_counts = item_counts

    @property
    def cost(self):
        return sum([cnt * item.cost for cnt,
                    item in zip(self.item_counts, self.items)])

    @property
    def volume(self):
        return sum([cnt * item.volume for cnt,
                    item in zip(self.item_counts, self.items)])

    def __repr__(self):
        return "[Стоимость {}; Предметы: {}]".format(
            self.cost, self.item_counts)


class Item:
    """
    Вещь.

    :param number: Порядковый номер вещи
    :param volume: Объем вещи
    :param cost: Стоимость вещи
    """

    def __init__(self, number: int, volume: int, cost: int):
        self.number = number
        self.volume = volume
        self.cost = cost

    def __repr__(self):
        return "[Вес: {}. Стоимость: {}]".format(self.volume, self.cost)
