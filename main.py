# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import core.sudoku as sud
import constants.const
import core.generator as gen


def main():
    # Generating of random Sudoku with 35 revealed cells
    sudoku_generated = gen.generate(n=35)
    print(sudoku_generated)

    # Example of solving default sudoku defined in constants
    data = constants.const.DEFAULT_SUDOKU
    size = constants.const.DEFAULT_DIM
    submatrix_size = constants.const.DEFAULT_SUBMATRIX_DIM

    # Initialize Sudoku object
    sudoku = sud.Sudoku(data, size=size, submatrix_dim=submatrix_size)

    # Solver which founds first available solution with randomness added
    sudoku.solve(randomness=True)
    print(sudoku)

    # Reset sudoku
    sudoku.reset()

    # Solver which founds all possible solutions if there are more
    solved, res = sudoku.find_all_solutions()
    print(len(res))
    print(solved)


if __name__ == '__main__':
    main()
