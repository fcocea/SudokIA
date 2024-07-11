import numpy as np


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
