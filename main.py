import csv
from pprint import pprint

SUDOKU_PUZZLE_FOLDER = "sudoku_puzzles"
DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# loads a Sudoku puzzle from a CSV and return a 9x9 2D list.
def load_puzzle_csv(filename):
    with open(f"{SUDOKU_PUZZLE_FOLDER}/{filename}", "r") as f:
        reader = csv.reader(f)
        puzzle = [[int(cell) for cell in row] for row in reader]
    return puzzle

# cehcks that every element in a list is unique, ignores zeros.
def has_unique_non_zeros(l):
    l_no_zeros = [i for i in l if i != 0]
    return len(l_no_zeros) == len(set(l_no_zeros))

# groups each 3x3 square into its own list.
def get_3x3s(puzzle):
    squares = []

    for square_row in range(3):
        for square_col in range(3):
            square = []
            
            for row in range(square_row * 3, square_row * 3 + 3):
                for col in range(square_col * 3, square_col * 3 + 3):
                    square.append(puzzle[row][col])
                    
            squares.append(square)
    return squares

# TODO: change this to only check a specfic value. 
def check_constraints(puzzle):
    for row in puzzle:
        if not has_unique_non_zeros(row):
            return False

    transposed = [list(row) for row in zip(*puzzle)]
    for col in transposed:
        if not has_unique_non_zeros(col):
            return False

    squares = get_3x3s(puzzle)
    for sq in squares:
        if not has_unique_non_zeros(sq):
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

def plain_backtrack(puzzle):
    if is_complete(puzzle):
        return puzzle

    var_row, var_col = get_next_unassigned(puzzle)
    for possible_value in DOMAIN:
        puzzle[var_row][var_col] = possible_value

        if check_constraints(puzzle):
            results = plain_backtrack(puzzle)
            if results != None:
                return results
        
        puzzle[var_row][var_col] = 0


    return None

pprint(plain_backtrack(load_puzzle_csv("easy.csv")))