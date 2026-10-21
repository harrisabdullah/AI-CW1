import csv
from pprint import pprint
import time
import sys

# Limit traceback output for cleaner error messages
sys.tracebacklimit = 2

SUDOKU_PUZZLE_FOLDER = "sudoku_puzzles"
BOARD_SIZE = 9

# Loads a Sudoku puzzle from a CSV and returns a 9x9 2D list of integers.
def load_puzzle_csv(filename):
    with open(f"{SUDOKU_PUZZLE_FOLDER}/{filename}", "r") as f:
        reader = csv.reader(f)
        puzzle = [[int(cell) for cell in row] for row in reader]
    return puzzle

# Calculates the base-2 logarithm using bitwise right shifts.
# Used to convert a binary flag (like 0b000010000) back to an integer (5).
def log2(n):
    log_val = 0
    while n > 1:
        n >>= 1
        log_val += 1
    return log_val

# Checks if a cell has exactly one possible value left.
# In binary, a power of 2 has only one '1' bit. 
# (n & (n - 1) == 0) is a quick bitwise trick to check if n is a power of 2.
def is_resolved(cell):
    return cell > 0 and (cell & (cell - 1)) == 0

# Applies a bitmask to a cell to remove a possibility.
# If removing this possibility leaves only one valid number (resolves the cell),
# it recursively updates other cells to reflect this new resolution.
def update_cell(bit_map, bit_mask, row, col):
    new = bit_map[row][col] & bit_mask
    
    # If the cell wasn't resolved before, but is resolved now, propagate the change
    if is_resolved(new) and not is_resolved(bit_map[row][col]):
        bit_map[row][col] = new
        update_bit_map(bit_map, row, col)
        
    bit_map[row][col] = new

# Yields the (row, col) coordinates of all cells in the same 3x3 block.
def get_square_index(row, col):
    square_row = (row // 3) * 3
    square_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            yield square_row + i, square_col + j

# When a cell is resolved, this function removes that cell's value from 
# all other cells in the same row, column, and 3x3 square using a bitwise NOT (~).
def update_bit_map(bit_map, row, col):
    bit_mask = ~bit_map[row][col]

    # Update the rest of the row and column
    for i in range(BOARD_SIZE):
        if i != col:
            update_cell(bit_map, bit_mask, row, i)
        if i != row:
            update_cell(bit_map, bit_mask, i, col)

    # Update the rest of the 3x3 square
    for r, c in get_square_index(row, col):
        if r == row and c == col:
            continue
        update_cell(bit_map, bit_mask, r, c)

# Initializes a 9x9 grid where every cell is 0b111111111 (511 in decimal).
# Each '1' bit represents a possible value from 1 to 9.
def generate_bit_map():
    return [[0b111111111 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Helper function to print the grid in its raw binary format for debugging.
def print_bit_map(bit_map):
    for row in bit_map:
        row_str = " ".join(f"{val:09b}" for val in row)
        print(row_str)

# Converts a standard integer Sudoku grid into a bitwise constraint grid.
# Applies the initial puzzle numbers and cascades their constraints.
def puzzle_to_bit_map(puzzle):
    bit_map = generate_bit_map()

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if puzzle[i][j] == 0:
                continue
                
            # Convert integer (e.g., 3) to bit flag (0b000000100)
            bit_map[i][j] = 1 << (puzzle[i][j] - 1)
            update_bit_map(bit_map, i, j)

    return bit_map

# Converts the resolved bitmask grid back into a standard integer grid.
def bit_map_to_puzzle(bit_map):
    puzzle = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if not is_resolved(bit_map[r][c]):
                return None
            
            # Convert bit flag back to integer (e.g., 0b000000100 -> 3)
            puzzle[r][c] = log2(bit_map[r][c]) + 1
    return puzzle

# Finds the first cell that has more than one possibility left.
def get_next_unresolved(bit_map):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if not is_resolved(bit_map[r][c]):
                return r, c
    return None

# Yields all possible integer values (1-9) still available in a cell's bitmask.
def get_domain(cell):
    for i in range(BOARD_SIZE):
        if cell & (1 << i) != 0:
            yield i + 1

# Recursively attempts to solve the puzzle by guessing valid options.
# Uses constraint propagation (update_bit_map) to aggressively reduce the search space.
def backtrack(bit_map, measures):
    unresolved = get_next_unresolved(bit_map)
    
    # Base case: No unresolved cells left, puzzle is solved
    if unresolved is None:
        return bit_map
    
    var_row, var_col = unresolved
    
    # If a cell has 0b0, it means all possibilities were eliminated (dead end)
    if bit_map[var_row][var_col] == 0b0:
        measures['backtrack_count'] += 1
        return None

    # Try every valid remaining number for this cell
    for possible_value in get_domain(bit_map[var_row][var_col]):
        measures['search_step'] += 1
        
        # Deep copy the current bit map state so we can safely guess
        temp = [row[:] for row in bit_map]
        
        # Make the guess and propagate the constraints
        temp[var_row][var_col] = 1 << (possible_value - 1)
        update_bit_map(temp, var_row, var_col)
        
        # Continue recursively
        solution = backtrack(temp, measures)
        if solution is not None:
            return solution
            
    return None

# Load and convert the puzzle to the bitmask representation
puzzle = load_puzzle_csv("easy.csv")
bit_map = puzzle_to_bit_map(puzzle)

start_time = time.perf_counter()

stats = {'search_step': 0, 'backtrack_count': 0}
s = backtrack(bit_map, stats)

end_time = time.perf_counter()

# Display results
pprint(stats)
pprint(bit_map_to_puzzle(s))
print(f"Elapsed time: {end_time - start_time} seconds")
