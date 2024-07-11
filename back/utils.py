from copy import deepcopy


def initialize_domains(board):
    """
    Inicializa los dominios de cada celda en el tablero de Sudoku.

    Parameters:
    board (list of list of int): El tablero de Sudoku.

    Returns:
    dict: Un diccionario con los dominios de cada celda.
    """
    domains = {}
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                domains[(r, c)] = list(range(1, 10))
            else:
                domains[(r, c)] = [board[r][c]]
    return domains

# Función para verificar si el tablero está completo


def is_complete(board):
    """
    Verifica si el tablero de Sudoku está completo.

    Parameters:
    board (list of list of int): El tablero de Sudoku.

    Returns:
    bool: True si el tablero está completo, False de lo contrario.
    """
    for row in board:
        if 0 in row:
            return False
    return True

# Función para verificar si un valor es consistente con las restricciones del Sudoku


def is_consistent(board, row, col, value):
    """
    Verifica si un valor es consistente con las restricciones del Sudoku.

    Parameters:
    board (list of list of int): El tablero de Sudoku.
    row (int): La fila de la celda.
    col (int): La columna de la celda.
    value (int): El valor a verificar.

    Returns:
    bool: True si el valor es consistente, False de lo contrario.
    """
    for i in range(9):
        if board[row][i] == value or board[i][col] == value:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == value:
                return False
    return True

# Función para realizar forward checking


def forward_checking(domains, row, col, value):
    """
    Realiza la propagación de restricciones eliminando valores del dominio de las celdas vecinas.

    Parameters:
    domains (dict): Los dominios de cada celda.
    row (int): La fila de la celda.
    col (int): La columna de la celda.
    value (int): El valor a asignar.

    Returns:
    dict: Un nuevo diccionario con los dominios actualizados.
    """
    new_domains = deepcopy(domains)
    for i in range(9):
        if value in new_domains[(row, i)]:
            new_domains[(row, i)].remove(value)
        if value in new_domains[(i, col)]:
            new_domains[(i, col)].remove(value)
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if value in new_domains[(start_row + i, start_col + j)]:
                new_domains[(start_row + i, start_col + j)].remove(value)
    return new_domains
