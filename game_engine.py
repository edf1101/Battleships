import random

import components


def attack(coordinates: tuple[int, int], board: list[list[str | None]], battleships: dict[str, int]) -> bool:
    """
    This function returns whether there is a ship hit when you fire at a location
    :param coordinates: Coordinates to check if there's a ship
    :param board: The board (list of lists) to check
    :param battleships: The list of enemy ships to decrement if there's a hit
    :return: Whether anything was hit
    """

    is_hit = board[coordinates[1]][coordinates[0]] is not None

    if is_hit:
        boat_type = board[coordinates[1]][coordinates[0]]
        battleships[boat_type] -= 1
        board[coordinates[1]][coordinates[0]] = None
        return True

    else:
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

        valid_input = x.isnumeric() and y.isnumeric() and int(x) >= 0 and int(y) >= 0

        if not valid_input:
            print("INVALID ENTRY - values must be positive and integers")

    x, y = int(x), int(y)
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

    print("---------------  GAME OVER --------------- ")
    print("#### THANK YOU FOR PLAYING BATTLESHIPS ###")


players = {}


def generate_attack(board: list[list[str | None]], attack_method: str = 'random') -> tuple[int, int]:
    """
    Generates a position to attack, via a chosen attack algorithm
    :param board: input the board to attack so the algorithm knows how large it is
    :param attack_method: What algorithm to choose a point, default 'random'
    :return: a tuple coordinate on the grid
    """

    if attack_method == 'random':
        # Purely random attack method
        x, y = random.randrange(0, len(board)), random.randrange(0, len(board))
        return x, y


def display_ascii(board: list[list[str | None]]) -> None:
    """
    Displays a given board on the command line
    :param board: The board to display
    :return: None, it prints the result
    """

    board_size = len(board)

    print('   ' + ''.join([f'  {i}   ' for i in range(board_size)]))  # Prints top numbers row

    for y in range(board_size):
        print('  ' + '-' * ((board_size * 6) + 1))  # divider on top of each row
        row = str(y) + " "

        for x in range(board_size):
            row += "|"  # Divider at the start of each cell

            if board[y][x] is not None:
                row += ' ### '  # wider cells so they are similar scaling width / height
            else:
                row += '     '

        row += '|'  # final divider on the end of rows
        print(row)
    print('  ' + '-' * ((board_size * 6) + 1))  # Bottom divider at the end


def ai_opponent_game_loop() -> None:
    """
    Plays a command line game of battleships against an AI
    :return: None
    """
    print("#### WELCOME TO BATTLESHIPS  AGAINST AI ###")

    # Initialise data
    players['Human'] = {'board': components.initialise_board(), 'ships': components.create_battleships()}
    players['AI'] = {'board': components.initialise_board(), 'ships': components.create_battleships()}

    # Place the ships
    players['Human']['board'] = components.place_battleships(players['Human']['board'],
                                                             players['Human']['ships'],
                                                             placement_method='custom')
    players['AI']['board'] = components.place_battleships(players['AI']['board'],
                                                          players['AI']['ships'],
                                                          placement_method='random')

    while count_ships_remaining(players['Human']['ships']) != 0 and count_ships_remaining(players['AI']['ships']) != 0:
        # Main game loop, continues as long as both players have ships (ie no one has won)
        print("-- USER'S TURN --")
        user_coords = cli_coordinates_input()
        attack_status = attack(user_coords, players['AI']['board'], players['AI']['ships'])
        if attack_status:
            print("You got a HIT!")
        else:
            print("You got a MISS!")

        print("-- AI'S TURN --")
        ai_coords = generate_attack(players['AI']['board'])
        attack_status = attack(ai_coords, players['Human']['board'], players['Human']['ships'])
        if attack_status:
            print("The AI got a HIT!")
        else:
            print("The AI got a MISS!")

        print(" Player's Board :")
        display_ascii(players['Human']['board'])

    if count_ships_remaining(players['Human']['ships']) == 0:
        print(" The Human LOST! Better luck next time")
    else:
        print(" The Human WON! Well done")


if __name__ == "__main__":
    ai_opponent_game_loop()
