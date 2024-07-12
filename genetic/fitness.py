def get_fitness(chromosome, failed=False):
    fitness = 0
    suspicious_cells = []

    for i in range(9):
        seen = {}  # Dictionary to track seen numbers and their positions
        for j in range(9):
            num = chromosome[j][i]
            if num in seen:
                fitness -= 1  # Decrease fitness for each duplicate
                # Add the first occurrence
                suspicious_cells.append((seen[num], i))
                suspicious_cells.append((j, i))  # Add the current duplicate
            seen[num] = j  # Store the position of the number

    # Check subgrids for duplicates (similar logic as for columns)
    for m in range(3):
        for n in range(3):
            seen = {}
            for i in range(3 * n, 3 * (n + 1)):
                for j in range(3 * m, 3 * (m + 1)):
                    num = chromosome[j][i]
                    if num in seen:
                        fitness -= 1
                        suspicious_cells.append((seen[num], i))
                        suspicious_cells.append((j, i))
                    seen[num] = j
    if failed:
        return fitness, suspicious_cells
    return fitness
