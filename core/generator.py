# Generating new random Sudoku puzzle
import constants.const as const
from core.sudoku import Sudoku
import numpy as np
import random
import copy


def generate(size: int = const.DEFAULT_DIM, submatrix_dim: int = const.DEFAULT_SUBMATRIX_DIM, n: int = 30) -> Sudoku:
    """
    Generator for Sudoku puzzle grids.

    :param size: Size of requested sudoku grid.
    :param submatrix_dim: Dimension of submatrixes in sudoku grid.
    :param n: Number of cells to remain.
    :return: Generated Sudoku.
    """
    # Generate randomly solved sudoku grid
    data = np.empty(size, np.ndarray)
    for i in range(size):
        data[i] = np.zeros(size, int)
    s = Sudoku(data, size, submatrix_dim)
    s.solve(randomness=True)

    s.data = copy.deepcopy(s.state)

    # get all positions in grid and number of cells
    coord = [i for i in range(size)]
    positions = combinations(coord, coord)
    num_cells = size*size

    # Try to remove number from random cell until number of revealed cells is lower that n or we have no positions to remove
    while num_cells > n and len(positions) > 0:
        # choose random position to try to remove number
        i = random.randint(0, len(positions)-1)
        row = positions[i][0]
        col = positions[i][1]
        positions = np.delete(positions, i, 0)

        # check if sudoku is still solvable and has unique solution after removing random position
        s.state[row][col] = 0
        solvable, res = s.find_all_solutions()
        if solvable and len(res) == 1:
            num_cells -= 1
            s.data[row][col] = 0
        else:
            s.state[row][col] = s.data[row][col]

    return s


def combinations(array1, array2) -> np.ndarray:
    """
    Get all combinations of elements from two arrays.

    :param array1:
    :param array2:
    :return: Array of combinations (pairs) of numbers.
    """
    mesh = np.array(np.meshgrid(array1, array2))
    combs = mesh.T.reshape(-1, 2)

    return combs
