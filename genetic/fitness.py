def get_fitness(chromosome):
    fitness = 0
    for i in range(9):
        seen = {}
        for j in range(9):
            if chromosome[j][i] in seen:
                seen[chromosome[j][i]] += 1
            else:
                seen[chromosome[j][i]] = 1
        for key in seen:
            fitness -= (seen[key] - 1)
    for m in range(3):
        for n in range(3):
            seen = {}
            for i in range(3 * n, 3 * (n + 1)):
                for j in range(3 * m, 3 * (m + 1)):
                    if chromosome[j][i] in seen:
                        seen[chromosome[j][i]] += 1
                    else:
                        seen[chromosome[j][i]] = 1
            for key in seen:
                fitness -= (seen[key] - 1)
    return fitness
