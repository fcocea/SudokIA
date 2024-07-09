import random as rndm

def make_gene(initial=None):
    if initial is None:
        initial = [0] * 9
    mapp = {}
    gene = list(range(1, 10))
    rndm.shuffle(gene)
    for i in range(9):
        mapp[gene[i]] = i
    for i in range(9):
        if initial[i] != 0 and gene[i] != initial[i]:
            temp = gene[i], gene[mapp[initial[i]]]
            gene[mapp[initial[i]]], gene[i] = temp
            mapp[initial[i]], mapp[temp[0]] = i, mapp[initial[i]]
    return gene

def make_chromosome(initial=None):
    if initial is None:
        initial = [[0] * 9] * 9
    chromosome = []
    for i in range(9):
        chromosome.append(make_gene(initial[i]))
    return chromosome

def make_population(count, initial=None):
    if initial is None:
        initial = [[0] * 9] * 9
    population = []
    for _ in range(count):
        population.append(make_chromosome(initial))
    return population