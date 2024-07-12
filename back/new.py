import csv
import time


def is_complete(board):
    return all(all(cell != 0 for cell in row) for row in board)


def is_valid(board, row, col, num):
    # Check row and column
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False

    # Check 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def get_unassigned_locations(board):
    if not all(len(row) == 9 for row in board):  # Check if all rows have length 9
        raise ValueError(
            "Invalid Sudoku puzzle: All rows must have 9 elements.")
    return [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]


def get_possible_values(board, row, col):
    return [num for num in range(1, 10) if is_valid(board, row, col, num)]


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


def backtrack(board, heuristic=None):
    if is_complete(board):
        return board

    if heuristic:
        next_cell = heuristic(board)
        if next_cell is None:
            return None
    else:
        unassigned = get_unassigned_locations(board)
        if not unassigned:
            return None
        next_cell = unassigned[0]

    row, col = next_cell
    possible_values = get_possible_values(board, row, col)
    for num in possible_values:
        board[row][col] = num
        if backtrack(board, heuristic):
            return board
        board[row][col] = 0

    return None


def combined_heuristic(board):
    unassigned = get_unassigned_locations(board)
    if not unassigned:
        return None

    # MRV: Find cells with the fewest possible values
    mrv_cells = min(unassigned, key=lambda x: len(
        get_possible_values(board, x)))
    min_domain_size = len(get_possible_values(board, mrv_cells))

    # LCV: Among MRV cells, find the one with the least constraining value
    best_cell = mrv_cells
    min_constraints = float('inf')
    for row, col in mrv_cells:
        for value in get_possible_values(board, row, col):
            constraints = count_constraints(board, row, col, value)
            if constraints < min_constraints:
                min_constraints = constraints
                best_cell = (row, col)

    return best_cell


def main():
    while True:
        try:
            num_puzzles_to_test = int(
                input("Enter the number of puzzles to test (or 0 to test all): "))
            if num_puzzles_to_test >= 0:
                break
            else:
                print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    total_times = {"normal": 0, "mrv": 0, "lcv": 0, "combined": 0}
    num_puzzles_solved = 0

    with open('../data/test.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for quiz_str, solution_str in reader:
            if num_puzzles_to_test == 0 or num_puzzles_solved < num_puzzles_to_test:
                # Convert puzzle and solution strings into 2D lists
                quiz = [list(map(int, quiz_str[i:i+9]))
                        for i in range(0, 81, 9)]
                solution = [list(map(int, solution_str[i:i+9]))
                            for i in range(0, 81, 9)]

                num_puzzles_solved += 1

                for method, heuristic in [
                    ("normal", None),
                    ("mrv", mrv_heuristic),
                    ("lcv", lcv_heuristic),
                    ("combined", combined_heuristic),
                ]:
                    # print(
                    # f"\nSolving puzzle {num_puzzles_solved} with {method}...")
                    start_time = time.time()
                    solved_board = backtrack(quiz.copy(), heuristic)
                    end_time = time.time()
                    total_times[method] += end_time - start_time

                    # if solved_board is not None:
                    #     print(f"Solved successfully using {method}.")
                    #     for row in solved_board:
                    #         print(row)
                    # else:
                    #     print(f"No solution found using {method}.")
            else:
                break

    # Display average runtimes
    print("\n--- Average Runtime Comparison ---")
    for method, total_time in total_times.items():
        average_time = total_time / num_puzzles_solved
        print(f"{method.upper()}: {average_time:.6f} seconds")
    print("-----------------------------------")


if __name__ == "__main__":
    main()
