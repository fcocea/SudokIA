def get_fitness(chromosome):
    fitness = 0
    for i in range(9):  # For each column
        seen = {}
        for j in range(9):  # Check each cell in the column
            if chromosome[j][i] in seen:
                seen[chromosome[j][i]] += 1
            else:
                seen[chromosome[j][i]] = 1
        for key in seen:  # Subtract fitness for repeated numbers
            fitness -= (seen[key] - 1)
    for m in range(3):  # For each 3x3 square
        for n in range(3):
            seen = {}
            for i in range(3 * n, 3 * (n + 1)):  # Check cells in 3x3 square
                for j in range(3 * m, 3 * (m + 1)):
                    if chromosome[j][i] in seen:
                        seen[chromosome[j][i]] += 1
                    else:
                        seen[chromosome[j][i]] = 1
            for key in seen:  # Subtract fitness for repeated numbers
                fitness -= (seen[key] - 1)
    return fitness
