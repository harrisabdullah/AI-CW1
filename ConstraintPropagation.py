import csv
from pprint import pprint
import time
import copy
import sys
sys.tracebacklimit = 2

SUDOKU_PUZZLE_FOLDER = "sudoku_puzzles"
BOARD_SIZE = 9

def load_puzzle_csv(filename):
    with open(f"{SUDOKU_PUZZLE_FOLDER}/{filename}", "r") as f:
        reader = csv.reader(f)
        puzzle = [[int(cell) for cell in row] for row in reader]
    return puzzle

def log2(n):
    log_val = 0
    while n > 1:
        n >>= 1
        log_val += 1
        
    return log_val

def is_resolved(cell):
    return cell > 0 and (cell & (cell - 1)) == 0

def update_cell(bit_map, bit_mask, row, col):
    new = bit_map[row][col] & bit_mask
    if is_resolved(new) and not is_resolved(bit_map[row][col]):
        bit_map[row][col] = new
        update_bit_map(bit_map, row, col)
    bit_map[row][col] = new

def get_square_index(row, col):
    square_row = (row // 3) * 3
    square_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            yield square_row + i, square_col + j

def update_bit_map(bit_map, row, col):
    bit_mask = ~bit_map[row][col]

    for i in range(BOARD_SIZE):
        if i != col:
            update_cell(bit_map, bit_mask, row, i)
        if i != row:
            update_cell(bit_map, bit_mask, i, col)

    for r, c in get_square_index(row, col):
        if r == row and c == col:
            continue
        update_cell(bit_map, bit_mask, r, c)

def genrate_bit_map():
    return [[0b111111111 for _ in range(9)] for _ in range(9)]

def print_bit_map(bit_map):
    for row in bit_map:
        row_str = " ".join(f"{val:09b}" for val in row)
        print(row_str)

def puzzle_to_bit_map(puzzle):
    bit_map = genrate_bit_map()

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if puzzle[i][j] == 0:
                continue
            bit_map[i][j] = 1 << (puzzle[i][j] - 1)
            update_bit_map(bit_map, i, j)

    return bit_map

def bit_map_to_puzzle(bit_map):
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    for r in range(9):
        for c in range(9):
            if not is_resolved(bit_map[r][c]):
                return None
            puzzle[r][c] = log2(bit_map[r][c]) + 1
    return puzzle

def get_next_unressolved(bit_map):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if not is_resolved(bit_map[r][c]):
                return r, c
    return None

def get_domain(cell):
    for i in range(9):
        if cell & (1 << i) != 0:
            yield i+1

def backtrack(bit_map, measures):
    unressolved = get_next_unressolved(bit_map)
    if unressolved is None:
        return bit_map
    
    var_row, var_col = unressolved
    if bit_map[var_row][var_col] == 0b0:
        measures['backtrack_count'] += 1
        return None

    for possible_value in get_domain(bit_map[var_row][var_col]):
        measures['search_step'] += 1
        temp = copy.deepcopy(bit_map)
        temp[var_row][var_col] = 1 << (possible_value - 1)
        update_bit_map(temp, var_row, var_col)
        
        solution = backtrack(temp, measures)
        if solution is not None:
            return solution
    return None

puzzle = load_puzzle_csv("hard.csv")
bit_map = puzzle_to_bit_map(puzzle)


start_time = time.perf_counter()

stats = {'search_step': 0, 'backtrack_count': 0}
s = backtrack(bit_map, stats)

end_time = time.perf_counter()
pprint(stats)
pprint(bit_map_to_puzzle(s))
print(f"Elapsed time: {end_time - start_time} seconds")