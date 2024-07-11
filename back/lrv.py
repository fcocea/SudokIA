import back.utils as utils


def least_constraining_value(domain, board, row, col):
    """
    Ordena los valores del dominio de una celda según el valor que impone la menor cantidad de restricciones en las celdas vecinas.

    Parameters:
    domain (dict): Los dominios de cada celda.
    board (list of list of int): El tablero de Sudoku.
    row (int): La fila de la celda.
    col (int): La columna de la celda.

    Returns:
    list: Los valores del dominio ordenados por menor restricción.
    """
    def count_constraints(value):
        constraints = 0
        for i in range(9):
            if board[row][i] == 0 and value in domain[(row, i)]:
                constraints += 1
            if board[i][col] == 0 and value in domain[(i, col)]:
                constraints += 1
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == 0 and value in domain[(start_row + i, start_col + j)]:
                    constraints += 1
        return constraints

    return sorted(domain[(row, col)], key=count_constraints)

# Algoritmo de Backtracking con Least Constraining Value (LCV)


def backtracking_with_lcv(board, domains):
    """
    Resuelve el Sudoku utilizando backtracking con la heurística LCV.

    Parameters:
    board (list of list of int): El tablero de Sudoku.
    domains (dict): Los dominios de cada celda.

    Returns:
    list of list of int: El tablero resuelto, o None si no se encuentra solución.
    """
    if utils.is_complete(board):
        return board
    # Seleccionar la primera celda vacía
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                row, col = r, c
                break
    for value in least_constraining_value(domains, board, row, col):
        if utils.is_consistent(board, row, col, value):
            board[row][col] = value
            new_domains = utils.forward_checking(
                board, domains, row, col, value)
            result = backtracking_with_lcv(board, new_domains)
            if result:
                return result
            board[row][col] = 0
    return None
