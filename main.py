import csv
from pprint import pprint
import time
import math

SUDOKU_PUZZLE_FOLDER = "sudoku_puzzles"
DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# loads a Sudoku puzzle from a CSV and return a 9x9 2D list.
def load_puzzle_csv(filename):
    with open(f"{SUDOKU_PUZZLE_FOLDER}/{filename}", "r") as f:
        reader = csv.reader(f)
        puzzle = [[int(cell) for cell in row] for row in reader]
    return puzzle

# checks that every element in a list is unique, ignores zeros.
def has_unique_non_zeros(l):
    l_no_zeros = [i for i in l if i != 0]
    return len(l_no_zeros) == len(set(l_no_zeros))

# groups each 3x3 square into its own list.
def get_3x3(puzzle, row, col):
    square_row = (row // 3) * 3
    square_col = (col // 3) * 3

    square = []
    for i in range(3):
        for j in range(3):
            square.append(puzzle[square_row + i][square_col + j])

    return square


def check_constraints(puzzle, row, col):
    if not has_unique_non_zeros(puzzle[row]):
        return False

    if not has_unique_non_zeros([i[col] for i in puzzle]):
        return False

    square = get_3x3(puzzle, row, col)
    if not has_unique_non_zeros(square):
        return False
    return True

def is_complete(puzzle):
    for row in puzzle:
        for i in row:
            if i == 0:
                return False
    return True

def get_next_unassigned(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == 0:
                return i, j
    return None

def plain_backtrack(puzzle, measures):
    if is_complete(puzzle):
        return puzzle

    var_row, var_col = get_next_unassigned(puzzle)
    for possible_value in DOMAIN:
        measures['search_step'] += 1
        puzzle[var_row][var_col] = possible_value

        if check_constraints(puzzle, var_row, var_col):
            solution = plain_backtrack(puzzle, measures)
            if solution is not None:
                return solution

        puzzle[var_row][var_col] = 0

    measures['backtrack_count'] += 1
    return None

start_time = time.perf_counter()

stats = {'search_step': 0, 'backtrack_count': 0}
s = plain_backtrack(load_puzzle_csv("hard.csv"), stats)
pprint(stats)

end_time = time.perf_counter()
pprint(s)
print(f"Elapsed time: {end_time - start_time} seconds")

