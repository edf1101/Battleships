"""
Functions used in gameplay
Also contains a single-player game if module is executed
"""
import logging

# Import battleships libs, pycharm likes it one way, terminal likes it the other
# using this try except bit here makes it work either way round
try:
    from battleships import components
except ImportError:
    import components

# Set up the logging
logging.basicConfig(filename='log', level=logging.DEBUG,
                    format="[%(asctime)s-%(levelname)s - %(funcName)20s() ] %(message)s",
                    filemode='a')


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

    # Check board param is set up correctly
    if not isinstance(board, list):
        logging.error('board should be a list of lists')
        raise TypeError('board should be a list of lists')
    for row in board:
        if not isinstance(row, list):
            logging.error('board should be a list of lists, one row isn\'t a list')
            raise TypeError('board should be a list of lists, one row isn\'t a list')
        for cell in row:
            if not (isinstance(cell, str) or cell is None):
                logging.error('each cell in the board should be None or a string')
                raise TypeError('each cell in the board should be None or a string')
    board_size = len(board)

    # Check coordinates is right type
    if (not isinstance(coordinates, tuple) or not isinstance(coordinates[0], int)
            or not isinstance(coordinates[1], int)):
        logging.error('coordinates is not a tuple of 2 ints')
        raise TypeError('coordinates is not a tuple of 2 ints')
    # Check coordinates is right length
    if len(coordinates) != 2:
        logging.error('coordinates tuple should be 2 ints long')
        raise ValueError('coordinates tuple should be 2 ints long')
    if not (0 <= coordinates[0] < board_size and 0 <= coordinates[1] < board_size):
        logging.error('coordinates out of the board')
        raise ValueError('coordinates out of the board')

    # Check the battleships dict
    if len(battleships) == 0:
        logging.error('battleships dict is empty')
        raise ValueError('battleships dict is empty')
    for key, value in battleships.items():
        if not isinstance(key,str) or not isinstance(value,int):
            logging.error('Dictionary keys/ values are not of type str then int')
            raise TypeError('Dictionary keys/ values are not of type str then int')

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

    x_co, y_co = 0, 0
    valid_input = False

    while not valid_input:

        x_co = input("What x coordinate?")
        y_co = input("What y coordinate?")

        valid_input = (x_co.isnumeric() and y_co.isnumeric()
                       and int(x_co) > 0 and int(y_co) > 0)

        if not valid_input:
            logging.warning(' user entered an invalid input of %s', {x_co, y_co})
            print("INVALID ENTRY - values must be positive and integers")

    x_co, y_co = int(x_co) - 1, int(y_co) - 1
    return x_co, y_co


def count_ships_remaining(ships: dict[str, int]) -> int:
    """
    Counts how many un-sunk tiles there are left

    :param ships: The dictionary of a player's ships
    :return: the number of ship tiles left
    """
    # Check the battleships dict
    if len(ships) == 0:
        raise ValueError('battleships dict is empty')
    for key, value in ships.items():
        if not isinstance(key, str) or not isinstance(value, int):
            raise TypeError('Dictionary keys/ values are not of type str then int')

    total = 0
    for partial_remaining in ships.values():
        total += partial_remaining

    return total


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

        coordinates = cli_coordinates_input()

        attack_status = attack(coordinates, board, ships)
        if attack_status:
            print("You got a HIT!")
        else:
            print("You got a MISS!")
        logging.debug('user got a %s', "hit" if attack_status else "miss")

    print("---------------  GAME OVER --------------- ")
    print("#### THANK YOU FOR PLAYING BATTLESHIPS ###")
    logging.debug('game_engine game over')


if __name__ == "__main__":
    logging.info('starting a game in game_engine.py')
    simple_game_loop()
