"""
Basic functions used mainly for setting up games
"""

import copy
import random
import json


def initialise_board(size: int = 10) -> list[list]:
    """
    Creates a blank board of size 'size'
    :param size: How big the board should be in both x and y directions
    :return: An empty list of lists (filled with None values)
    """

    try:  # Check the size is an int
        size = int(size)
    except ValueError as e:
        raise TypeError("size should be of type int") from e

    if size < 1:
        raise ValueError("Size must be ≥ 1")

    board = []
    for _ in range(size):
        row = [None for x in range(size)]
        board.append(row)
    return board


def create_battleships(filename: str = "battleships.txt") -> dict[str, int]:
    """
    This function extracts the battleship data from a file
    :param filename: The file to read ship data from
    :return: A dictionary with the ships' names and sizes
    """

    with open(filename, 'r', encoding="utf-8") as file:
        data = file.read()

    data = data.split('\n')  # each new line should be data entry

    battleships = {}
    for item in data:
        name, size = item.split(':')

        if not isinstance(name, str):  # Check the keys are strings
            raise ValueError("battleships.txt error one key isn't of type str")

        try:  # Check the sizes are ints
            size = int(size.strip())
        except ValueError as e:
            raise ValueError("battleships.txt error one value isn't of type int") from e

        battleships[str(name)] = size

    return battleships


def try_place_ship(board: list[list],
                   ship_name: str,
                   ship_size: int,
                   position: tuple[int, int],
                   orientation: str) -> list[list[str | None]] | None:
    """
    Used for the random placement method in place_battleships function
    :param board: A list of lists representing the board
    :param ship_name: The name of the ship being placed
    :param ship_size: The size of the ship being placed
    :param position: starting position of the ship
    :param orientation: what direction the ship faces  'v' = down, 'h' = right
    :return: None if the placement is invalid, else the updated board list of lists
    """

    # Check for incorrect parameters
    if (not isinstance(orientation, str) or not isinstance(ship_size, int)
            or not isinstance(ship_name, str)
            or not isinstance(board, list)):
        raise TypeError('Incorrect argument type')

    # Check for incorrect board argument
    for row in board:
        if not isinstance(row, list):
            raise TypeError('board argument incorrect')

    # Check for incorrect position argument
    if (not isinstance(position, tuple) or not isinstance(position[0], int)
            or not isinstance(position[1], int)):
        raise TypeError('position argument incorrect')

    # Check orientation is correct
    if orientation not in ['v','h']:
        raise ValueError('orientation should be v or h')

    modify_board = copy.deepcopy(board)  # so it doesn't modify the board passed through parameters
    for _ in range(ship_size):

        if 0 <= position[0] < len(board) and 0 <= position[1] < len(board):
            pass  # inside board
        else:
            return None  # out of bounds of the board

        if board[position[1]][position[0]] is None:
            pass  # empty space
        else:
            return None  # on another ship

        modify_board[position[1]][position[0]] = ship_name

        if orientation == 'v':  # Down
            position = (position[0], position[1] + 1)

        elif orientation == 'h':  # Right
            position = (position[0] + 1, position[1])
        else:
            raise ValueError("Orientation can only be 'v' or 'h'")

    return modify_board


def place_battleships(board: list[list],
                      ships: dict[str, int],
                      algorithm: str = 'simple') -> list[list[str]]:
    """
    Places all the ships onto the board using a specified placement algorithm
    :param board: A list of lists representing the board
    :param ships: A dictionary of ships in the game and their sizes
    :param algorithm: either 'simple', 'random' or 'custom'
    :return: A list of lists representing the board, with tiles filled where ships are
    """

    # Error checking to see if any of the arguments are present but bad
    if not isinstance(board, list) or not isinstance(ships, dict):
        raise TypeError('parameter type error')

    if len(board) == 0 or len(board[0]) == 0:
        raise ValueError('Board parameter is of size 0')

    if len(ships) == 0:
        raise ValueError('ships parameter is of size 0')

    # Basic placement algorithm as seen in specification
    if algorithm == 'simple':

        row = 0
        for ship_name, ship_size in ships.items():

            for x in range(ship_size):
                board[row][x] = ship_name
            row += 1  # go down a row

        return board

    # Ships will be placed with random position + orientation, as long as they fit
    if algorithm == 'random':
        for ship_name, ship_size in ships.items():

            # First guess at a position
            position = (random.randrange(0, len(board)), random.randrange(0, len(board)))
            orientation = random.choice(['v', 'h'])
            potential_placement = try_place_ship(board, ship_name, ship_size, position, orientation)

            while potential_placement is None:  # try random spots until one is valid
                position = (random.randrange(0, len(board)), random.randrange(0, len(board)))
                orientation = random.choice(['v', 'h'])
                potential_placement = try_place_ship(board,
                                                     ship_name,
                                                     ship_size,
                                                     position,
                                                     orientation)

            board = potential_placement
        return board

    # Ships will be placed with a position and orientation as specified in a JSON file
    if algorithm == 'custom':

        with open('placement.json', 'r', encoding="utf-8") as file:
            json_data = json.loads(file.read())

        ship_names = list(json_data.keys())

        for ship_name in ship_names:

            # example file had a dict of ship_name : [position.x,position.y,orientation]
            ship_position = (int(json_data[ship_name][0]), int(json_data[ship_name][1]))
            ship_orientation = json_data[ship_name][2]

            potential_placement = try_place_ship(board, ship_name,
                                                 ships[ship_name],
                                                 ship_position,
                                                 ship_orientation)
            if potential_placement is None:
                raise ValueError("Supplied JSON data doesn't fit in the board")

            board = potential_placement

        return board

    raise ValueError('Invalid Argument for algorithm parameter')


def in_board(location: tuple[int, int], board: list[list]) -> bool:
    """
    Returns whether a point is inside the board or not
    :param location: The point to query
    :param board: Reference to the board so we can find it's size
    :return: Whether its inside
    """

    if not isinstance(board, list) or not isinstance(location, tuple):
        raise TypeError('parameter type error')

    if not isinstance(location[0], int) or not isinstance(location[1], int):
        raise TypeError('incorrect location parameter format')

    if len(location) != 2:
        raise ValueError('incorrect location parameter length')

    inside = 0 <= location[0] < len(board) and 0 <= location[1] < len(board)
    return inside
