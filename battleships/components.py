"""
Basic functions used mainly for setting up games
"""

import copy
import random
import json
import os
import logging

# Set up the logging
logging.basicConfig(filename='log', level=logging.DEBUG,
                    format="[%(asctime)s-%(levelname)s - %(funcName)20s() ] %(message)s",
                    filemode='a')


def initialise_board(size: int = 10) -> list[list]:
    """
    Creates a blank board of size 'size'

    :param size: How big the board should be in both x and y directions
    :return: An empty list of lists (filled with None values)
    """

    if not isinstance(size, int):
        logging.error("size should be of type int")
        raise TypeError("size should be of type int")

    if size < 1:
        logging.error("Size must be ≥ 1")
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

    if not isinstance(filename, str):
        logging.error('filename parameter should be a string')
        raise TypeError('filename parameter should be a string')

    # recreate filename using absolute path
    working_directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(working_directory, filename)

    try:
        with open(filename, 'r', encoding="utf-8") as file:
            data = file.read()
    except FileNotFoundError as ex:
        logging.error("filename doesn't exist")
        raise ValueError(f"filename {filename} doesn't exist") from ex

    data = data.split('\n')  # each new line should be data entry

    battleships = {}
    for item in data:
        name, size = item.split(':')

        try:  # Check the sizes are ints
            size = int(size.strip())
        except ValueError as exc:
            logging.error("battleships.txt error one value isn't of type int")
            raise ValueError("battleships.txt error one value isn't of type int") from exc

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
        logging.error('Incorrect argument type')
        raise TypeError('Incorrect argument type')

    # Check for incorrect board argument
    for row in board:
        if not isinstance(row, list):
            logging.error('board argument incorrect')
            raise TypeError('board argument incorrect')

    # Check for incorrect position argument
    if (not isinstance(position, tuple) or not isinstance(position[0], int)
            or not isinstance(position[1], int)):
        logging.error('position argument incorrect')
        raise TypeError('position argument incorrect')

    # Check orientation is correct
    if orientation not in ['v', 'h']:
        logging.error('orientation should be v or h')
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

    return modify_board


def place_battleships(board: list[list],
                      ships: dict[str, int],
                      algorithm: str = 'simple',
                      use_absolute_path: bool = True) -> list[list[str]]:
    """
    Places all the ships onto the board using a specified placement algorithm

    :param board: A list of lists representing the board
    :param ships: A dictionary of ships in the game and their sizes
    :param algorithm: either 'simple', 'random' or 'custom'
    :param use_absolute_path: Should it use a relative or absolute path (for pytest)
    :return: A list of lists representing the board, with tiles filled where ships are
    """

    # Error checking to see if any of the arguments are present but bad
    if not isinstance(board, list) or not isinstance(ships, dict):
        logging.error('parameter type error')
        raise TypeError('parameter type error')

    if len(board) == 0 or len(board[0]) == 0:
        logging.error('Board parameter is of size 0')
        raise ValueError('Board parameter is of size 0')

    if len(ships) == 0:
        logging.error('ships parameter is of size 0')
        raise ValueError('ships parameter is of size 0')

    # Basic placement algorithm as seen in specification
    if algorithm == 'simple':

        row = 0
        for ship_name, ship_size in ships.items():

            for x_co in range(ship_size):
                board[row][x_co] = ship_name
            row += 1  # go down a row

        return board

    # Ships will be placed with random position + orientation, as long as they fit
    if algorithm == 'random':
        return place_battleships_random(board, ships)

    # Ships will be placed with a position and orientation as specified in a JSON file
    if algorithm == 'custom':
        return place_battleships_custom(board, ships, use_absolute_path)

    logging.error('Invalid Argument for algorithm parameter')
    raise ValueError('Invalid Argument for algorithm parameter')


def place_battleships_random(board: list[list],
                             ships: dict[str, int]) -> list[list[str]]:
    """
    Places all the ships onto the board using a random placement

    :param board: A list of lists representing the board
    :param ships: A dictionary of ships in the game and their sizes
    :return: A list of lists representing the board, with tiles filled where ships are
    """
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


def place_battleships_custom(board: list[list],
                             ships: dict[str, int],
                             use_absolute_path: bool = True) -> list[list[str]]:
    """
    Places all the ships onto the board using a custom placement algorithm

    :param board: A list of lists representing the board
    :param ships: A dictionary of ships in the game and their sizes
    :param use_absolute_path: Should it use a relative or absolute path (for pytest)
    :return: A list of lists representing the board, with tiles filled where ships are
    """

    # pytest doesn't like the use of absolute paths, so we'll create an optional argument
    # to not use it with that
    if use_absolute_path:
        # recreate placement.json filename using absolute path
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'placement.json'),
                  'r', encoding="utf-8") as file:
            json_data = json.loads(file.read())
    else:
        # use relative path placement.json
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
            logging.error("Supplied JSON data doesn't fit in the board")
            raise ValueError("Supplied JSON data doesn't fit in the board")

        board = potential_placement

    return board


def in_board(location: tuple[int, int], board: list[list]) -> bool:
    """
    Returns whether a point is inside the board or not

    :param location: The point to query
    :param board: Reference to the board so we can find it's size
    :return: Whether its inside
    """

    if not isinstance(board, list) or not isinstance(location, tuple):
        logging.error('parameter type error')
        raise TypeError('parameter type error')

    if not isinstance(location[0], int) or not isinstance(location[1], int):
        logging.error('incorrect location parameter format')
        raise TypeError('incorrect location parameter format')

    if len(location) != 2:
        logging.error('incorrect location parameter length')
        raise ValueError('incorrect location parameter length')

    inside = 0 <= location[0] < len(board) and 0 <= location[1] < len(board)
    return inside


def get_positions_by_name(board: list[list], names: list[str]) -> list[tuple[int, int]]:
    """
    Returns a list of all the tuple positions on the board that are occupied by a ship
    with name in list names. Primarily used for finding sunk ships

    :param board: The board to search in
    :param names: The names of the ships to look for
    :return: A list of the positions with name in list 'names'
    """
    # Check parameters
    if not isinstance(board, list) or not isinstance(names, list):
        logging.error('parameters are incorrect type')
        raise TypeError('parameters are incorrect type')
    # Check that each row of the board list is also a list
    for row in board:
        if not isinstance(row, list):
            logging.error('parameter board is not a list of lists')
            raise TypeError('parameter board is not a list of lists')

    positions = []
    for row_idx, row in enumerate(board):
        for idx, cell in enumerate(row):

            if cell in names:  # If the cell name is in names
                positions.append((idx, row_idx))  # Append the tuple of its coordinates

    return positions


def get_sunken_ships(player_data: dict) -> list[tuple[int, int]]:
    """
    Calculate which of a player's ships we have sunk based on its original board

    :param player_data: The dict containing boards, ships etc.
    :return: A list of positions that have been sunk
    """
    if ('ships' not in player_data or 'original_board' not in player_data
            or not isinstance(player_data, dict)):
        logging.error('incomplete player data variable')
        raise ValueError('incomplete player data variable')

    sunk_ship_types = [k for k, v in player_data['ships'].items() if v == 0]
    sunken_places = get_positions_by_name(player_data['original_board'],
                                          sunk_ship_types)
    return sunken_places
