"""
Functions used in gameplay
Also contains a single-player game if module is executed
"""

from copy import deepcopy
import components


def attack(coordinates: tuple[int, int],
           board: list[list[str | None]],
           battleships: dict[str, int]) -> bool:
    """
    This function returns whether there is a ship hit when you fire at a location
    :param coordinates: Coordinates to check if there's a ship
    :param board: The board (list of lists) to check
    :param battleships: The list of enemy ships to decrement if there's a hit
    :return: Bool Whether anything was hit
    """

    is_hit = board[coordinates[1]][coordinates[0]] is not None

    if is_hit:
        boat_type = board[coordinates[1]][coordinates[0]]
        battleships[boat_type] -= 1
        board[coordinates[1]][coordinates[0]] = None
        return True

    return False


def cli_coordinates_input() -> tuple[int, int]:
    """
    Requests the user for input coordinates then returns the tuple position
    :return: returns the tuple position of inputted coordinates
    """

    x, y = 0, 0
    valid_input = False

    while not valid_input:

        x = input("What x coordinate?")
        y = input("What y coordinate?")

        valid_input = x.isnumeric() and y.isnumeric() and int(x) > 0 and int(y) > 0

        if not valid_input:
            print("INVALID ENTRY - values must be positive and integers")

    x, y = int(x) - 1, int(y) - 1
    return x, y


def count_ships_remaining(ships: dict[str, int]) -> int:
    """
    Counts how many un-sunk tiles there are left
    :param ships: The dictionary of a player's ships
    :return: the number of ship tiles left
    """
    total = 0
    for partial_remaining in ships.values():
        total += partial_remaining

    return total

# Functions below are for the extension 'storm' functionality (board moves each turn)
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

    for row_ind, _ in enumerate(board):  # Go through each row

        modify_row = board[row_ind].copy()
        for cell_index, _ in enumerate(board):
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

    for _ in range(dir_y):
        board = shift_down(board)

    for _ in range(dir_x):
        board = shift_right(board)

    return board



def simple_game_loop() -> None:
    """
    Plays a single player game in the command line
    :return: None
    """

    print("#### WELCOME TO BATTLESHIPS ###")
    board = components.initialise_board()
    ships = components.create_battleships()
    board = components.place_battleships(board, ships)

    while count_ships_remaining(ships) > 0:

        # Input validation for the coordinates, check they're in board range
        coordinates = (-1, -1)
        while not (0 <= coordinates[0] < len(board) and 0 <= coordinates[1] < len(board)):
            coordinates = cli_coordinates_input()
            while not (0 <= coordinates[0] < len(board) and 0 <= coordinates[1] < len(board)):
                coordinates = cli_coordinates_input()
                if not (0 <= coordinates[0] < len(board) and 0 <= coordinates[1] < len(board)):
                    print("Coordinates outside of the board")

        attack_status = attack(coordinates, board, ships)
        if attack_status:
            print("You got a HIT!")
        else:
            print("You got a MISS!")

    print("---------------  GAME OVER --------------- ")
    print("#### THANK YOU FOR PLAYING BATTLESHIPS ###")


if __name__ == "__main__":
    simple_game_loop()
