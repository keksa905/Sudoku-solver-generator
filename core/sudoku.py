# main class for sudoku
import numpy as np
import constants.const as const
from random import shuffle
import copy


class Sudoku:
    """
    Main class for representation of Sudoku.
    """

    def __init__(self, init_data: np.ndarray = const.DEFAULT_SUDOKU, size: int = const.DEFAULT_DIM,
                 submatrix_dim: int = const.DEFAULT_SUBMATRIX_DIM) -> None:
        """
        Initialization method.

        :param init_data: Data for initialization of new sudoku array.
        :param size: Dimension of sudoku grid.
        :param submatrix_dim: Dimension of submatrix where the numbers has to be checked.
        :return:
        """

        if init_data is None or size is None or submatrix_dim is None:
            self.data = const.DEFAULT_SUDOKU
            self.size = const.DEFAULT_DIM
            self.submatrix_dim = const.DEFAULT_SUBMATRIX_DIM
            self.state = const.DEFAULT_SUDOKU
            self.checked = False
            return

        # check if array has valid dimension
        if len(init_data) != size:
            raise ValueError(f"Wrong number of rows in sudoku data: {len(init_data)}, but expected {size}")
        else:
            for i, row in enumerate(init_data):
                if not isinstance(row, np.ndarray):
                    raise ValueError(f"Wrong init data format: array of arrays is expected, but {i}. row is {type(row)}")
                elif len(row) != size:
                    raise ValueError(f"Wrong number of columns in {i}. row: {len(row)}, but expected {size}")

        if size % submatrix_dim != 0:
            raise ValueError(
                f"Wrong submatrix dimension, it should divide dimension but dimension is {size} and submatrix dimension is {submatrix_dim}")

        self.data = copy.deepcopy(init_data)
        self.size = size
        self.submatrix_dim = submatrix_dim
        self.state = copy.deepcopy(init_data)
        self.checked = False
        return

    def __str__(self) -> str:
        """
        Overrides string representation of class.
        :return: String representation.
        """
        final_string = ""
        for i in range(self.size):
            if i % self.submatrix_dim == 0:
                final_string += 3 * self.size * "-" + "\n"
            for j in range(self.size):
                if j % self.submatrix_dim == 0:
                    final_string += "| "
                final_string += f"{self.state[i][j]} "
            final_string += "| \n"

        final_string += 3*self.size * "-" + "\n"
        # return str(self.state)
        return final_string

    def reset(self):
        """
        Reset Sudoku state to init state.

        :return: None.
        """
        self.state = copy.deepcopy(self.data)

    def solve(self, randomness: bool = False) -> bool:
        """
        Method for solving Sudoku based on backtracking.

        :return: Boolean if sudoku is solved or it cannot be solved.
        """
        # check if sudoku is valid if it is not checked yet
        if not self.checked:
            if not self.is_valid():
                return False

        # Check if there is still some free position
        row, column = self.first_free_pos()
        if row is None or column is None:
            return True

        numbers = [i for i in range(1, self.size + 1)]
        if randomness:
            shuffle(numbers)

        for number in numbers:
            if self.is_valid_element(row, column, number):
                self.state[row][column] = number
                solved = self.solve(randomness=randomness)
                if solved:
                    return True

        self.state[row][column] = 0

        return False

    def find_all_solutions(self) -> (bool, []):
        """
        Method for solving Sudoku based on backtracking which finds all possible solutions.

        :return: Boolean if sudoku is solved or it cannot be solved.
        :return: Array of all solutions.
        """
        # check if sudoku is valid if it is not checked yet
        if not self.checked:
            if not self.is_valid():
                return False, []

        solutions = []
        solved = False

        # Check if there is still some free position
        row, column = self.first_free_pos()
        if row is None or column is None:
            solutions.append(self.state.copy())
            return True, solutions

        for number in range(1, self.size + 1):
            if self.is_valid_element(row, column, number):
                self.state[row][column] = number
                sol, res = self.find_all_solutions()
                if sol:
                    solved = True
                    solutions.extend(res)

        self.state[row][column] = 0

        return solved, solutions

    def first_free_pos(self) -> (int, int):
        """
        Finds first free position of sudoku grid.

        :return: Tuple of position of first free position in current state (row, column). If there is no free position, (None, None) is returned.
        """

        for row in range(self.size):
            for column in range(self.size):
                if self.state[row][column] == 0:
                    return row, column

        return None, None

    def is_valid_element(self, row: int, column: int, number: int) -> bool:
        """
        Checks if given number on given position of sudoku is valid. Number has to be unique in row, in column and in submatrix.

        :param row: Row position of number.
        :param column: Column position of number.
        :param number: Number to checks if it is valid.
        :return: Boolean if the number is valid or not.
        """
        # Check uniqueness in row
        for i in range(self.size):
            if i == column:
                continue
            if self.state[row][i] == number:
                return False

        # Check uniqueness in column
        for i in range(self.size):
            if i == row:
                continue
            if self.state[i][column] == number:
                return False

        # Check uniqueness in submatrix
        submatrix_row_start = row - (row % self.submatrix_dim)
        submatrix_column_start = column - (column % self.submatrix_dim)
        for i in range(submatrix_row_start, submatrix_row_start + self.submatrix_dim):
            for j in range(submatrix_column_start, submatrix_column_start + self.submatrix_dim):
                if i == row and j == column:
                    continue
                if self.state[i][j] == number:
                    return False

        return True

    def is_valid(self) -> bool:
        """
        Checks if current state of sudoku is valid.

        :return: Boolean if Sudoku is valid or not.
        """
        self.checked = True
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 0:
                    continue
                if not self.is_valid_element(i, j, self.state[i][j]):
                    return False

        return True
