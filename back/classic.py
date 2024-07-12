from back.utils import is_complete, get_unassigned_locations, get_possible_values
import numpy as np


def backtracking(board, heuristic=None):
    print(np.array(board))
    if is_complete(board):
        return board
    if heuristic:
        next_cell = heuristic(board)
        print('next', next_cell)
        if next_cell is None:
            return None
    else:
        unassigned = get_unassigned_locations(board)
        if not unassigned:
            return None
        next_cell = unassigned[0]
    row, col = next_cell
    print('next cell', next_cell)
    possible_values = get_possible_values(board, row, col)
    for num in possible_values:
        board[row][col] = num
        if backtracking(board, heuristic) is not None:
            return board
        board[row][col] = 0
    return None
