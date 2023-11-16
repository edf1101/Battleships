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
    except ValueError:
        raise ValueError("size should be of type int")

    if size < 1:
        raise ValueError("Size must be ≥ 1")

    board = []
    for y in range(size):
        row = [None for x in range(size)]
        board.append(row)
    return board


def create_battleships(filename: str = "battleships.txt") -> dict[str, int]:
    """
    This function extracts the battleship data from a file
    :param filename: The file to read ship data from
    :return: A dictionary with the ships' names and sizes
    """

    with open(filename, 'r') as file:
        data = file.read()

    data = data.split('\n')  # each new line should be data entry

    battleships = {}
    for item in data:
        name, size = item.split(':')

        if type(name) != str:  # Check the keys are strings
            raise ValueError("battleships.txt error one key isn't of type str")

        try:  # Check the sizes are ints
            size = int(size.strip())
        except ValueError:
            raise ValueError("battleships.txt error one value isn't of type int")

        battleships[str(name)] = size

    return battleships


def try_place_ship(board: list[list],
                   ship_name: str,
                   ship_size: int,
                   position: tuple[int, int],
                   orientation: str) -> list[list[str | None]] | None:  # Require version ≥ 3.10 due to '|' type hinting
    """
    Used for the random placement method in place_battleships function
    :param board: A list of lists representing the board
    :param ship_name: The name of the ship being placed
    :param ship_size: The size of the ship being placed
    :param position: starting position of the ship
    :param orientation: what direction the ship faces  'v' = down, 'h' = right
    :return: None if the placement is invalid, else the updated board list of lists
    """

    modify_board = copy.deepcopy(board)  # so it doesn't modify the board passed through parameters
    for i in range(ship_size):

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


def place_battleships(board: list[list], ships: dict[str, int], placement_method: str = 'simple') -> list[list[str]]:
    """
    Places all the ships onto the board using a specified placement algorithm
    :param board: A list of lists representing the board
    :param ships: A dictionary of ships in the game and their sizes
    :param placement_method: either 'simple', 'random' or 'custom'
    :return: A list of lists representing the board, with tiles filled where ships are
    """

    # Basic placement algorithm as seen in specification
    if placement_method == 'simple':

        row = 0
        for ship_name, ship_size in ships.items():

            for x in range(ship_size):
                board[row][x] = ship_name
            row += 1  # go down a row

        return board

    # Ships will be placed with random position + orientation, as long as they fit
    elif placement_method == 'random':
        for ship_name, ship_size in ships.items():

            # First guess at a position
            position = (random.randrange(0, len(board)), random.randrange(0, len(board)))
            orientation = random.choice(['v', 'h'])
            potential_placement = try_place_ship(board, ship_name, ship_size, position, orientation)

            while potential_placement is None:  # try random spots until one is valid
                position = (random.randrange(0, len(board)), random.randrange(0, len(board)))
                orientation = random.choice(['v', 'h'])
                potential_placement = try_place_ship(board, ship_name, ship_size, position, orientation)

            board = potential_placement
        return board

    # Ships will be placed with a position and orientation as specified in a JSON file
    elif placement_method == 'custom':

        with open('placement.json', 'r') as file:
            json_data = json.loads(file.read())

        ship_names = [i for i in json_data.keys()]

        for ship_name in ship_names:

            # example file had a dict of ship_name : [position.x,position.y,orientation]
            ship_position = (int(json_data[ship_name][0]), int(json_data[ship_name][1]))
            ship_orientation = json_data[ship_name][2]

            potential_placement = try_place_ship(board, ship_name, ships[ship_name], ship_position, ship_orientation)
            if potential_placement is None:
                raise ValueError("Supplied JSON data doesn't fit in the board")

            else:
                board = potential_placement
    return board
