import back.utils as utils


def select_unassigned_variable_mrv(board, domains):
    """
    Selecciona la celda vacía con el menor número de valores posibles en su dominio (MRV).

    Parameters:
    board (list of list of int): El tablero de Sudoku.
    domains (dict): Los dominios de cada celda.

    Returns:
    tuple: La posición (fila, columna) de la celda seleccionada.
    """
    min_domain_size = float('inf')
    selected_var = None
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:  # Si la celda está vacía
                domain_size = len(domains[(r, c)])
                if domain_size < min_domain_size:
                    min_domain_size = domain_size
                    selected_var = (r, c)
    return selected_var


def backtracking_with_mrv(board, domains):
    """
    Resuelve el Sudoku utilizando backtracking con la heurística MRV.

    Parameters:
    board (list of list of int): El tablero de Sudoku.
    domains (dict): Los dominios de cada celda.

    Returns:
    list of list of int: El tablero resuelto, o None si no se encuentra solución.
    """
    if utils.is_complete(board):
        return board
    var = select_unassigned_variable_mrv(board, domains)
    if var is None:
        return None
    row, col = var
    for value in domains[(row, col)]:
        if utils.is_consistent(board, row, col, value):
            board[row][col] = value
            print(board)
            new_domains = utils.forward_checking(domains, row, col, value)
            result = backtracking_with_mrv(board, new_domains)
            if result:
                return result
            board[row][col] = 0
    return None
