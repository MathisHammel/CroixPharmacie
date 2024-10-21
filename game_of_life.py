import itertools
import random
import sys
import time
from typing import List

import pygame

from pharmacontroller import SCREEN_SIZE, PharmaScreen

Grid = type(List[List[int]])


def is_valid_index(row: int, column: int) -> bool:
    """
    Check if the given row and column are valid indices.

    Args:
        row (int): The row index.
        column (int): The column index.

    Returns:
        bool: True if the indices are valid, False otherwise.
    """
    conditions = (
        0 <= row < SCREEN_SIZE,
        0 <= column < SCREEN_SIZE,
        PharmaScreen.is_drawable(row, column),
    )
    return all(conditions)


def generate_grid() -> Grid:
    """
    Generate a grid without any living cells.

    Returns:
        List[List[int]]: The grid state.
    """
    return [[0 for _ in range(SCREEN_SIZE)] for _ in range(SCREEN_SIZE)]


def get_neighbors(grid: Grid, row: int, column: int) -> List[int]:
    """
    Get the neighbors of the cell at the given row and column.

    Args:
        grid (numpy.ndarray): The grid state.
        row (int): The row of the cell.
        column (int): The column of the cell.

    Returns:
        List[int]: The list of neighbors.
    """
    neighbors = []

    # Iterate over the 3x3 grid around the cell
    for i, j in itertools.product(range(-1, 2), repeat=2):
        # Ignore current cell
        if i == 0 and j == 0:
            continue

        # Get the new row and column
        new_row = row + i
        new_column = column + j

        # Ignore out of bounds cells
        if not is_valid_index(new_row, new_column):
            continue

        neighbors.append(grid[new_row][new_column])

    return neighbors


def next_generation(grid: Grid) -> Grid:
    """
    Generate the next generation of the grid.

    Returns:
        List[List[int]]: The next generation of the grid.
    """
    new_grid = generate_grid()

    for row, column in itertools.product(range(SCREEN_SIZE), range(SCREEN_SIZE)):
        neighbors = get_neighbors(grid, row, column)
        alive_neighbors = sum(neighbors)
        cell = grid[row][column]

        if cell == 1:
            if alive_neighbors < 2 or alive_neighbors > 3:
                new_grid[row][column] = 0  # Cell dies of underpopulation or overpopulation
            else:
                new_grid[row][column] = 1  # Cell survives
        else:
            if alive_neighbors == 3:
                new_grid[row][column] = 1  # Cell is born (good population)

    return new_grid


if __name__ == "__main__":
    pygame.init()
    screen = PharmaScreen(color_scale=False)

    grid = generate_grid()

    for _ in range(500):
        grid[random.randrange(SCREEN_SIZE)][random.randrange(SCREEN_SIZE)] = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        grid = next_generation(grid)
        screen.set_image(grid)

        # Leave time to contemplate life
        time.sleep(0.1)
