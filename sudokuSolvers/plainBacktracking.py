import csv
from pprint import pprint
import sys
import time

SUDOKU_PUZZLE_FOLDER = "sudoku_puzzles"
DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# loads a Sudoku puzzle from a CSV and returns a 9x9 2D list
def load_puzzle_csv(filename):
    with open(f"{SUDOKU_PUZZLE_FOLDER}/{filename}", "r") as f:
        reader = csv.reader(f)
        puzzle = [[int(cell) for cell in row] for row in reader]
    return puzzle

# checks that every element in a list is unique, ignores zeros
def has_unique_non_zeros(l):
    l_no_zeros = [i for i in l if i != 0]
    return len(l_no_zeros) == len(set(l_no_zeros))

# groups each 3x3 square into its own list
def get_3x3(puzzle, row, col):
    # determine the starting row and column index of the 3x3 subgrid
    square_row = (row // 3) * 3
    square_col = (col // 3) * 3

    square = []
    for i in range(3):
        for j in range(3):
            square.append(puzzle[square_row + i][square_col + j])

    return square

# checks the row colum and 3x3 grid around a given cell
def check_constraints(puzzle, row, col):
    # check if the current row is valid
    if not has_unique_non_zeros(puzzle[row]):
        return False

    # check if the current column is valid by extracting the col-th element from every row
    if not has_unique_non_zeros([i[col] for i in puzzle]):
        return False

    # check if the local 3x3 grid is valid
    square = get_3x3(puzzle, row, col)
    if not has_unique_non_zeros(square):
        return False
        
    return True

# check if all cells in a puzzle are filled
def is_complete(puzzle):
    # a puzzle is complete when there are no empty cells (represented by 0) left
    for row in puzzle:
        for i in row:
            if i == 0:
                return False
    return True

# gets the next empty cell
def get_next_unassigned(puzzle):
    # scan the grid row by row to find the first empty cell
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == 0:
                return i, j
    return None

def plain_backtrack(puzzle, measures):
    # base case: if the puzzle is completely filled we found the solution
    if is_complete(puzzle):
        return puzzle

    # get the coordinates of the next empty cell
    var_row, var_col = get_next_unassigned(puzzle)
    
    # try every possible number
    for possible_value in DOMAIN:
        measures['search_step'] += 1
        
        # make a guess
        puzzle[var_row][var_col] = possible_value

        # if the guess doesn't break any Sudoku rules continue recursively
        if check_constraints(puzzle, var_row, var_col):
            solution = plain_backtrack(puzzle, measures)
            
            # if the recursive call found a solution return it up the call stack
            if solution is not None:
                return solution

        # if the guess led to a dead end backtrack and try the next number
        puzzle[var_row][var_col] = 0

    # if all numbers fail for this cell backtrack
    measures['backtrack_count'] += 1
    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python script.py <filename.csv>")

    filename = sys.argv[1]
    measures = {'search_step': 0, 'backtrack_count': 0}
    
    start_time = time.time()

    puzzle = load_puzzle_csv(filename)
    solved_puzzle = plain_backtrack(puzzle, measures)

    pprint(solved_puzzle if solved_puzzle else "No solution found.")
    
    print(f"\nTime: {time.time() - start_time:.4f}s")
    print(f"Steps: {measures['search_step']} | Backtracks: {measures['backtrack_count']}")
