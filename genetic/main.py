import genes as gn
import genetic_algorithm as ga
import fitness as ft
import time

ch = gn.make_chromosome()
print(ft.get_fitness(ch))

def pch(ch):
    for i in range(9):
        for j in range(9):
            print(ch[i][j], end=" ")
        print("")

tic = time.time()
#modificar con dataset
r = ga.genetic_algorithm("./sample_sudoku/Test2.txt")
toc = time.time()
print("time_taken: ", toc - tic)
fit = [ft.get_fitness(c) for c in r]
m = max(fit)
print(max(fit))

# Print the chromosome with the highest fitness
for c in r:
    if ft.get_fitness(c) == m:
        pch(c)
        break

