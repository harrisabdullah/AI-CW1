import csv
from pprint import pprint
import time
import sys

SUDOKU_PUZZLE_FOLDER = "sudoku_puzzles"
BOARD_SIZE = 9

# loads a Sudoku puzzle from a CSV and returns a 9x9 2D list
def load_puzzle_csv(filename):
    with open(f"{SUDOKU_PUZZLE_FOLDER}/{filename}", "r") as f:
        reader = csv.reader(f)
        puzzle = [[int(cell) for cell in row] for row in reader]
    return puzzle

# calculates log base 2 using bit shifts
# used to turn a bit flag back into an integer
def log2(n):
    log_val = 0
    # keep shifting right and counting until only the first 1 bit is left
    while n > 1:
        n >>= 1
        log_val += 1
    return log_val

# checks if a cell has exactly one possible value left
# a power of 2 only has one 1 bit so (n & (n - 1)) is 0 when n is a power of 2
def is_resolved(cell):
    return cell > 0 and (cell & (cell - 1)) == 0

# removes possibilities from a cell using a bitmask
# if this leaves the cell with only one number we have to update its neigbours
def update_cell(bit_map, bit_mask, row, col):
    # remove the possibilities that are in the mask
    new = bit_map[row][col] & bit_mask
    
    # if the cell wasn't resolved before but is now propogate the change
    if is_resolved(new) and not is_resolved(bit_map[row][col]):
        bit_map[row][col] = new
        update_bit_map(bit_map, row, col)
        
    bit_map[row][col] = new

# yields the row and col of every cell in the same 3x3 square
def get_square_index(row, col):
    # determine the starting row and column index of the 3x3 grid
    square_row = (row // 3) * 3
    square_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            yield square_row + i, square_col + j

# when a cell is resolved remove its value from the row colum and 3x3 square around it
def update_bit_map(bit_map, row, col):
    # flip the bits so the resolved value is the one that gets removed
    bit_mask = ~bit_map[row][col]

    # update the rest of the row and column
    for i in range(BOARD_SIZE):
        if i != col:
            update_cell(bit_map, bit_mask, row, i)
        if i != row:
            update_cell(bit_map, bit_mask, i, col)

    # update the rest of the 3x3 square
    for r, c in get_square_index(row, col):
        # skip the cell itself
        if r == row and c == col:
            continue
        update_cell(bit_map, bit_mask, r, c)

# makes a 9x9 grid where every cell starts as 0b111111111
# each 1 bit means that number (1-9) is still possible
def generate_bit_map():
    return [[0b111111111 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# turns a normal Sudoku puzzle into a bit map and propagates the constraints from the starting numbers.
def puzzle_to_bit_map(puzzle):
    bit_map = generate_bit_map()

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # 0 means the cell is empty so skip it
            if puzzle[i][j] == 0:
                continue
                
            # turn the number into a bit flag
            bit_map[i][j] = 1 << (puzzle[i][j] - 1)
            # remove that number from the cells around it
            update_bit_map(bit_map, i, j)

    return bit_map

# turns the bit map back into a normal 9x9 puzzle
def solved_bit_map_to_puzzle(bit_map):
    puzzle = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            # if any cell is not resolved there is no full solution
            if not is_resolved(bit_map[r][c]):
                return None
            
            # turn the bit flag back into a number
            puzzle[r][c] = log2(bit_map[r][c]) + 1
    return puzzle

# gets the next cell that still has more than one possibility
def get_next_unresolved(bit_map):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if not is_resolved(bit_map[r][c]):
                return r, c
    return None

# yields every number that is still possible in a cell
def get_domain(cell):
    for i in range(BOARD_SIZE):
        if cell & (1 << i) != 0:
            yield i + 1

# backtracking that uses constraint propagation
def backtrack(bit_map, measures):
    unresolved = get_next_unresolved(bit_map)
    
    # base case: if every cell is resolved we found the solution
    if unresolved is None:
        return bit_map
    
    # get the coordinates of the next unresolved cell
    var_row, var_col = unresolved
    
    # if a cell has no possibilities left its a dead end
    if bit_map[var_row][var_col] == 0b0:
        measures['backtrack_count'] += 1
        return None

    # try every number that is still possible
    for possible_value in get_domain(bit_map[var_row][var_col]):
        measures['search_step'] += 1
        
        # copy the bit map so we can make a guess without messing up the original
        temp = [row[:] for row in bit_map]
        
        # make a guess and propogate it to the other cells
        temp[var_row][var_col] = 1 << (possible_value - 1)
        update_bit_map(temp, var_row, var_col)
        
        solution = backtrack(temp, measures)
        # if the recursive call found a solution return it
        if solution is not None:
            return solution
            
    # if all numbers fail for this cell backtrack
    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python script.py <filename.csv>")

    filename = sys.argv[1]
    measures = {'search_step': 0, 'backtrack_count': 0}
    
    start_time = time.time()

    solved_bit_map = backtrack(puzzle_to_bit_map(load_puzzle_csv(filename)), measures)

    pprint(solved_bit_map_to_puzzle(solved_bit_map) if solved_bit_map else "No solution found.")

    print(f"\nTime: {time.time() - start_time:.4f}s")
    print(f"Steps: {measures['search_step']} | Backtracks: {measures['backtrack_count']}")
