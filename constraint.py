from main import load_puzzle_csv
import math
import copy
import time
import csv
from pprint import pprint

def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0

def is_valid_solution(bit_map):
    # A valid Sudoku group will have exactly bits 1 through 9 set: 511
    for i in range(9):
        row_or = 0
        col_or = 0
        for j in range(9):
            row_or |= bit_map[i][j]
            col_or |= bit_map[j][i]
        if row_or != 511 or col_or != 511:
            return False
            
    # Check 3x3 squares
    for sq_row in range(0, 9, 3):
        for sq_col in range(0, 9, 3):
            sq_or = 0
            for i in range(3):
                for j in range(3):
                    sq_or |= bit_map[sq_row + i][sq_col + j]
            if sq_or != 511:
                return False
                
    return True

def genrate_bit_map():
    return [[0b111111111 for _ in range(9)] for _ in range(9)]

def print_bit_map(bit_map):
    for row in bit_map:
        # Format each integer as a 9-bit binary string separated by spaces
        row_str = " ".join(f"{val:09b}" for val in row)
        print(row_str)

def eliminate_possibility(cell, value):
    return cell & ~(1 << (value - 1))

def update_bit_map(bit_map, value, row, col):
    for i, cell in enumerate(bit_map[row]):
        bit_map[row][i] = eliminate_possibility(cell, value)

    for i in range(9):
        bit_map[i][col] = eliminate_possibility(bit_map[i][col], value)

    square_row = (row // 3) * 3
    square_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            offset_row = square_row + i
            offset_col = square_col + j
            bit_map[offset_row][offset_col] = eliminate_possibility(bit_map[offset_row][offset_col], value)

    bit_map[row][col] = 1 << (value - 1)

def puzzle_to_bit_map(puzzle):
    bit_map = genrate_bit_map()

    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                continue
            update_bit_map(bit_map, puzzle[i][j], i, j)

    return bit_map

def log2(n: int) -> int:
    
    log_val = 0
    while n > 1:
        n >>= 1    # Shift bits right by 1 (equivalent to integer division by 2)
        log_val += 1
        
    return log_val

def bit_map_to_puzzle(bit_map):
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if not is_power_of_two(bit_map[i][j]):
                return None
            puzzle[i][j] = log2(bit_map[i][j]) + 1
    return puzzle

def is_complete(bit_map):
    for i in range(9):
        for j in range(9):
            if not is_power_of_two(bit_map[i][j]):
                return False
    return True

def get_next_unassigned(bit_map):
    for i in range(9):
        for j in range(9):
            if not is_power_of_two(bit_map[i][j]):
                return i, j
    return None

def get_domain(cell):
    domain = []
    for i in range(9):
        if cell & (1 << i) != 0:
            domain.append(i+1)
    return domain

def new_backtrack(bit_map, measures):
    unassigned = get_next_unassigned(bit_map)
    
    # If NO unassigned cells are left (all cells are powers of 2)
    if unassigned is None:
        # Verify that these options don't contain silent duplicates
        if is_valid_solution(bit_map):
            return bit_map
        else:
            measures['backtrack_count'] += 1
            return None

    var_row, var_col = unassigned
    domain = get_domain(bit_map[var_row][var_col])

    if not domain:
        measures['backtrack_count'] += 1
        return None

    for possible_value in domain:
        temp = copy.deepcopy(bit_map)
        measures['search_step'] += 1
        update_bit_map(temp, possible_value, var_row, var_col)
        
        solution = new_backtrack(temp, measures)
        if solution is not None:
            return solution

    return None

puzzle = load_puzzle_csv("hard.csv")
bit_map = puzzle_to_bit_map(puzzle)


start_time = time.perf_counter()

stats = {'search_step': 0, 'backtrack_count': 0}
s = new_backtrack(bit_map, stats)

end_time = time.perf_counter()
pprint(stats)
pprint(bit_map_to_puzzle(s))
print(f"Elapsed time: {end_time - start_time} seconds")