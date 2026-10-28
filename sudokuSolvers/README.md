# Ai-CW1
This project uses python 3.14 and contains three programs: `main.py`, `plainBacktracking.py` and `constraintPropagation.py`.

## External Libraries
The main program requires pandas and matplotlib. No other program requires external libraries.

## Usage
### main
Usage: `python main.py`

`main` is run directly and will test plain backtracking against constraint propagation using the `sudoku-examples.csv` dataset and plot the results.

### plainBacktracking
Usage: `python plainBacktracking.py {filename.csv}`

`{filename.csv}` should be a csv file containing a 9x9 grid of integers between 1 and 9.

`plainBacktracking` will search for `{filename.csv}` in the `sudoku_puzzles` directory and attempt to solve the puzzle using plain backtracking. It will print the solved puzzle, backtrack count, search steps and runtime.

### constraintPropagation
Usage: `python constraintPropagation.py {filename.csv}`

`{filename.csv}` should be a csv file containing a 9x9 grid of integers between 1 and 9.

`constraintPropagation` will search for `{filename.csv}` in the `sudoku_puzzles` directory and attempt to solve the puzzle using backtracking with constraint propagation. It will print the solved puzzle, backtrack count, search steps and runtime.
