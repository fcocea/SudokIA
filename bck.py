import numpy as np
import pandas as pd

data = pd.read_csv('data/data-1.csv').to_numpy()[0]
sudoku, solution = np.reshape([int(c) for c in data[0]], (9, 9)), np.reshape([int(c) for c in data[1]], (9, 9))


def is_valid(game: np.ndarray, row: int, col: int, num: int) -> bool:
    for i in range(9):
        if game[row][i] == num or game[i][col] == num:
            return False
    for i in range(3):
        for j in range(3):
            if game[(row // 3) * 3 + i][(col // 3) * 3 + j] == num:
                return False
    return True


def solve(game: np.ndarray) -> bool:
    for i in range(9):
        for j in range(9):
            if game[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(game, i, j, num):
                        game[i][j] = num
                        if solve(game):
                            return True
                        game[i][j] = 0
                return False
    return True


solve(sudoku)
print(sudoku)

print(np.array_equal(sudoku, solution))
