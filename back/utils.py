def is_complete(board):
    return all(all(cell != 0 for cell in row) for row in board)


def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def get_unassigned_locations(board):
    return [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]


def get_possible_values(board, row, col):
    return [num for num in range(1, 10) if is_valid(board, row, col, num)]


def combined_heuristic(board):
    unassigned = get_unassigned_locations(board)
    if not unassigned:
        return None
    mrv_cells = min(unassigned, key=lambda x: len(
        get_possible_values(board, x[0], x[1])))
    best_cell = mrv_cells
    min_constraints = float('inf')
    row, col = mrv_cells
    for value in get_possible_values(board, row, col):
        constraints = count_constraints(board, row, col, value)
        if constraints < min_constraints:
            min_constraints = constraints
            best_cell = (row, col)
    return best_cell


def count_constraints(board, row, col, num):
    constraints = 0
    for x in range(9):
        if board[row][x] == 0 and is_valid(board, row, x, num):
            constraints += 1
        if board[x][col] == 0 and is_valid(board, x, col, num):
            constraints += 1
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == 0 and is_valid(board, start_row + i, start_col + j, num):
                constraints += 1
    return constraints
