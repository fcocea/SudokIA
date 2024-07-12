import random as rndm
import genetic.genes as gn
import genetic.fitness as ft
import genetic.mutation as mt


def r_get_mating_pool(population):
    fitness_list = []
    pool = []
    for chromosome in population:
        fitness = ft.get_fitness(chromosome)
        fitness_list.append((fitness, chromosome))
    fitness_list.sort()
    weight = list(range(1, len(fitness_list) + 1))
    for _ in range(len(population)):
        ch = rndm.choices(fitness_list, weight)[0]
        pool.append(ch[1])
    return pool


def w_get_mating_pool(population):
    fitness_list = []
    pool = []
    for chromosome in population:
        fitness = ft.get_fitness(chromosome)
        fitness_list.append((fitness, chromosome))
    weight = [fit[0] - fitness_list[0][0] for fit in fitness_list]
    for _ in range(len(population)):
        ch = rndm.choices(fitness_list, weights=weight)[0]
        pool.append(ch[1])
    return pool


def get_offsprings(population, initial, pm, pc):
    new_pool = []
    i = 0
    while i < len(population):
        ch1 = population[i]
        ch2 = population[(i + 1) % len(population)]
        x = rndm.randint(0, 100)
        if x < pc * 100:
            ch1, ch2 = mt.crossover(ch1, ch2)
        new_pool.append(mt.mutation(ch1, pm, initial))
        new_pool.append(mt.mutation(ch2, pm, initial))
        i += 2
    return new_pool


def genetic_algorithm(board):
    ## Hyperparameters ##
    # Population size
    POPULATION = 1000
    # Number of generations
    REPETITION = 1000
    # Probability of mutation
    PM = 0.1
    # Probability of crossover
    PC = 0.95

    population = gn.make_population(POPULATION, board)
    for _ in range(REPETITION):
        mating_pool = r_get_mating_pool(population)
        rndm.shuffle(mating_pool)
        population = get_offsprings(mating_pool, board, PM, PC)
        fit = [ft.get_fitness(c) for c in population]
        m = max(fit)
        if m == 0:
            for c in population:
                if ft.get_fitness(c) == m:
                    return c
    for c in population:
        if ft.get_fitness(c) == m:
            return c
