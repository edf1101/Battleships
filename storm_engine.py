"""
This module holds a few functions for shifting lists of lists
This is useful for the storm game-mode where the board shifts each turn
"""
from copy import deepcopy


def shift_down(board: list[list]) -> list[list]:
    """
    Shifts a list of lists down 1 space
    :param board: The list to shift
    :return: The shifted list
    """
    board_write = deepcopy(board)  # deep copy of the board we'll write to

    for i in range(len(board)):
        board_write[i] = board[i - 1]  # Swap with one above it

    return board_write


def shift_right(board:list[list]) -> list[list]:
    """
    Shifts a list of lists right 1 space
    :param board: The list to shift
    :return: The shifted list
    """
    board = deepcopy(board)  # deep copy of the board we'll write to so we don't modify original

    for row_ind in range(len(board)):  # Go through each row

        modify_row = board[row_ind].copy()
        for cell_index in range(len(modify_row)):
            modify_row[cell_index] = board[row_ind][cell_index - 1]

        board[row_ind] = modify_row

    return board


def shift(board:list[list], direction:tuple[int, int]) -> list[list]:
    """
    Shifts a board in any direction
    :param board: The board to shift
    :param direction: how many spaces in each x,y direction to move
    :return: The shifted board
    """

    # This bit makes it able to handle large and negative numbers in either direction
    dir_y = (direction[1] + len(board)) % len(board)
    dir_x = (direction[0] + len(board)) % len(board)

    for i in range(dir_y):
        board = shift_down(board)

    for i in range(dir_x):
        board = shift_right(board)

    return board
