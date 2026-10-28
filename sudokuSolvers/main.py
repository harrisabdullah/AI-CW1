from constraintPropagation import backtrack as constraint_backtrack, puzzle_to_bit_map, solved_bit_map_to_puzzle
from plainBacktracking import plain_backtrack
import csv
import json
import time
import copy
import pandas as pd
import matplotlib.pyplot as plt

BLUE = "#4878D0"
ORANGE = "#EE854A"

# loads the puzzles from a CSV and returns a list of [id, puzzle, solution, difficulty]
def load_sudoku_data(input_file_path):
    loaded_data = []

    with open(input_file_path, mode='r', encoding='utf-8') as f:
        # DictReader lets us get each column by its name
        reader = csv.DictReader(f)

        for row in reader:
            puzzle_id = int(row['id'])
            # the puzzle and solution are stored as json strings so we parse them into 2D lists
            puzzle = json.loads(row['puzzle_2d'])
            solution = json.loads(row['solution_2d'])
            difficulty = float(row['difficulty'])

            loaded_data.append([puzzle_id, puzzle, solution, difficulty])

    return loaded_data


# runs both solvers on every puzzle and records the time steps and backtracks, returns a DataFrame
def evaluate_solvers(data):
    results = []

    for puzzle_id, puzzle, solution, difficulty in data:

        # run the plain backtracking solver
        measures_plain = {"backtrack_count": 0, "search_step": 0}
        # copy the puzzle because plain backtracking changes it in place
        puzzle_copy = copy.deepcopy(puzzle)
        start_time = time.perf_counter()
        solved_plain = plain_backtrack(puzzle_copy, measures_plain)
        plain_time = time.perf_counter() - start_time
        # check if the answer matches the known solution
        plain_correct = (solved_plain == solution)

        # run the constraint propagation solver
        measures_constraint = {"backtrack_count": 0, "search_step": 0}
        # turn the puzzle into a bit map first, this happens before the timer starts
        bitmap_puzzle = puzzle_to_bit_map(puzzle)
        start_time = time.perf_counter()
        solved_bitmap = constraint_backtrack(bitmap_puzzle, measures_constraint)
        constraint_time = time.perf_counter() - start_time
        # turn the bit map back into a normal puzzle, None means no solution was found
        solved_constraint = solved_bit_map_to_puzzle(solved_bitmap) if solved_bitmap is not None else None
        constraint_correct = (solved_constraint == solution)

        # save everything for this puzzle as one row
        results.append({
            "id": puzzle_id,
            "difficulty": difficulty,

            "plain_time": plain_time,
            "plain_steps": measures_plain["search_step"],
            "plain_backtracks": measures_plain["backtrack_count"],
            "plain_correct": plain_correct,

            "constraint_time": constraint_time,
            "constraint_steps": measures_constraint["search_step"],
            "constraint_backtracks": measures_constraint["backtrack_count"],
            "constraint_correct": constraint_correct
        })

    return pd.DataFrame(results)


# draws plain and constraint on the same scatter plot, difficulty is always the x axis
def scatter_comparison(df, plain_col, constraint_col):
    plt.scatter(df['difficulty'], df[plain_col], label='Plain',
                color=BLUE, alpha=0.6, s=36, edgecolors='none')
    plt.scatter(df['difficulty'], df[constraint_col], label='Constraint',
                color=ORANGE, alpha=0.6, s=36, edgecolors='none')


# prints how many puzzles each solver got wrong then makes all the plots
def plot_performance(df):
    # set a cleaner look for all the plots
    plt.rcParams.update({
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": "0.85",
        "axes.edgecolor": "0.8",
        "xtick.major.size": 0,
        "ytick.major.size": 0,
    })

    # count the puzzles where the solver did not match the known solution
    failed_plain = df[~df['plain_correct']].shape[0]
    failed_constraint = df[~df['constraint_correct']].shape[0]
    print(f"results:")
    print(f"plain backtrack failed on {failed_plain} puzzles.")
    print(f"constraint backtrack failed on {failed_constraint} puzzles.\n")

    # leave out the 0.0 difficulty puzzles for the scatter plots, the bar chart still uses all of them
    df_scatter = df[df['difficulty'] > 0.0]

    # plot 1: runtime vs difficulty
    plt.figure(figsize=(10, 6))
    scatter_comparison(df_scatter, 'plain_time', 'constraint_time')
    # log scale because the values are spread out so much
    plt.yscale('log')
    plt.title('Runtime vs Difficulty (Log Scale)', fontsize=14, weight='bold')
    plt.ylabel('Time (Seconds)')
    plt.xlabel('Difficulty Rating')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # plot 2: search steps vs difficulty
    plt.figure(figsize=(10, 6))
    scatter_comparison(df_scatter, 'plain_steps', 'constraint_steps')
    plt.yscale('log')
    plt.title('Search Steps vs Difficulty (Log Scale)', fontsize=14, weight='bold')
    plt.ylabel('Total Search Steps')
    plt.xlabel('Difficulty Rating')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # plot 3: backtracks vs difficulty
    plt.figure(figsize=(10, 6))
    scatter_comparison(df_scatter, 'plain_backtracks', 'constraint_backtracks')
    plt.yscale('log')
    plt.title('Number of Backtracks vs Difficulty (log Scale)', fontsize=14, weight='bold')
    plt.ylabel('Number of Backtracks')
    plt.xlabel('Difficulty Rating')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # plot 4: bar chart of the average runtime across every puzzle
    plt.figure(figsize=(10, 6))
    avg_times = [df['plain_time'].mean(), df['constraint_time'].mean()]
    bars = plt.bar(['Plain Backtrack', 'Constraint Backtrack'], avg_times, color=[BLUE, ORANGE], width=0.6)
    plt.title('Average Runtime Across All Puzzles (Includes 0.0 Difficulty)', fontsize=14, weight='bold')
    plt.ylabel('Average Time (Seconds)')

    # write the average value on top of each bar
    for bar, v in zip(bars, avg_times):
        plt.text(bar.get_x() + bar.get_width() / 2, v, f'{v:.5f}s', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.show()


# prints the average time steps and backtracks for both solvers and the diffrence between them
def print_summary_statistics(df):
    # average of each measure across all puzzles
    mean_plain_time = df['plain_time'].mean()
    mean_constraint_time = df['constraint_time'].mean()

    mean_plain_steps = df['plain_steps'].mean()
    mean_constraint_steps = df['constraint_steps'].mean()

    mean_plain_backtracks = df['plain_backtracks'].mean()
    mean_constraint_backtracks = df['constraint_backtracks'].mean()

    # difference is plain minus constraint so a positive number means constraint did better
    print(f"Runtime:")
    print(f"plain: {mean_plain_time:.5f}s")
    print(f"Constraint: {mean_constraint_time:.5f}s")
    print(f"difference: {mean_plain_time - mean_constraint_time:.5f}s\n")

    print(f"search steps:")
    print(f"Plain: {mean_plain_steps:.1f}")
    print(f"Constraint: {mean_constraint_steps:.1f}")
    print(f" Difference: {mean_plain_steps - mean_constraint_steps:.1f}\n")

    print(f"backtracks:")
    print(f"Plain: {mean_plain_backtracks:.1f}")
    print(f"constraint: {mean_constraint_backtracks:.1f}")
    print(f"difference: {mean_plain_backtracks - mean_constraint_backtracks:.1f}\n")


# load all the puzzles
sudoku_data = load_sudoku_data("sudoku-examples.csv")

# run both solvers on every puzzle
print(f"Evaluating {len(sudoku_data)} puzzles...")
results_df = evaluate_solvers(sudoku_data)
# show the stats first then the plots
print_summary_statistics(results_df)

plot_performance(results_df)
