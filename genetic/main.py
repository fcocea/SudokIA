import genetic.genes as gn
import genetic.genetic_algorithm as ga
import genetic.fitness as ft
import time

ch = gn.make_chromosome()
print(ft.get_fitness(ch))


def pch(ch):
    for i in range(9):
        for j in range(9):
            print(ch[i][j], end=" ")
        print("")


def solve():
    tic = time.time()
    r = ga.genetic_algorithm()
    toc = time.time()
    print("time_taken: ", toc - tic)

    fit = [ft.get_fitness(c) for c in r]
    m = max(fit)
    print(max(fit))
    for c in r:
        if ft.get_fitness(c) == m:
            pch(c)
            break
