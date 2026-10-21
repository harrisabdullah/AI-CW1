import csv
from pprint import pprint
import time
import math

SUDOKU_PUZZLE_FOLDER = "sudoku_puzzles"
DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Loads a Sudoku puzzle from a CSV and returns a 9x9 2D list.
def load_puzzle_csv(filename):
    with open(f"{SUDOKU_PUZZLE_FOLDER}/{filename}", "r") as f:
        reader = csv.reader(f)
        puzzle = [[int(cell) for cell in row] for row in reader]
    return puzzle

# Checks that every element in a list is unique, ignores zeros.
def has_unique_non_zeros(l):
    l_no_zeros = [i for i in l if i != 0]
    return len(l_no_zeros) == len(set(l_no_zeros))

# Groups each 3x3 square into its own list.
def get_3x3(puzzle, row, col):
    # Determine the starting row and column index of the 3x3 subgrid
    square_row = (row // 3) * 3
    square_col = (col // 3) * 3

    square = []
    for i in range(3):
        for j in range(3):
            square.append(puzzle[square_row + i][square_col + j])

    return square


def check_constraints(puzzle, row, col):
    # Check if the current row is valid
    if not has_unique_non_zeros(puzzle[row]):
        return False

    # Check if the current column is valid by extracting the 'col'-th element from every row
    if not has_unique_non_zeros([i[col] for i in puzzle]):
        return False

    # Check if the local 3x3 grid is valid
    square = get_3x3(puzzle, row, col)
    if not has_unique_non_zeros(square):
        return False
        
    return True

def is_complete(puzzle):
    # A puzzle is complete when there are no empty cells (represented by 0) left
    for row in puzzle:
        for i in row:
            if i == 0:
                return False
    return True

def get_next_unassigned(puzzle):
    # Scan the grid row by row to find the first empty cell
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == 0:
                return i, j
    return None

def plain_backtrack(puzzle, measures):
    # Base case: if the puzzle is completely filled, we found the solution
    if is_complete(puzzle):
        return puzzle

    # Get the coordinates of the next empty cell to process
    var_row, var_col = get_next_unassigned(puzzle)
    
    # Try plugging in every possible number (1-9)
    for possible_value in DOMAIN:
        measures['search_step'] += 1
        
        # Make a guess
        puzzle[var_row][var_col] = possible_value

        # If the guess doesn't break any Sudoku rules, continue recursively
        if check_constraints(puzzle, var_row, var_col):
            solution = plain_backtrack(puzzle, measures)
            
            # If the recursive call found a solution, return it up the call stack
            if solution is not None:
                return solution

        # If the guess led to a dead end, undo it (backtrack) and try the next number
        puzzle[var_row][var_col] = 0

    # If all numbers 1-9 fail for this cell, trigger a backtrack to the previous cell
    measures['backtrack_count'] += 1
    return None

start_time = time.perf_counter()

# Dictionary to pass performance metrics by reference so they update during recursion
stats = {'search_step': 0, 'backtrack_count': 0}

# Run the backtracking algorithm
s = plain_backtrack(load_puzzle_csv("easy.csv"), stats)

pprint(stats)

end_time = time.perf_counter()
pprint(s)
print(f"Elapsed time: {end_time - start_time} seconds")
