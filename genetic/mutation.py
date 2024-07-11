import random as rndm
import genetic.genes as gn


def crossover(ch1, ch2):
    new_child_1 = []
    new_child_2 = []
    for i in range(9):
        x = rndm.randint(0, 1)
        if x == 1:
            new_child_1.append(ch1[i])
            new_child_2.append(ch2[i])
        elif x == 0:
            new_child_2.append(ch1[i])
            new_child_1.append(ch2[i])
    return new_child_1, new_child_2


def mutation(ch, pm, initial):
    for i in range(9):
        x = rndm.randint(0, 100)
        if x < pm * 100:
            ch[i] = gn.make_gene(initial[i])
    return ch
