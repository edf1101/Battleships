"""
Contains functions needed for a multiplayer game, ie generating attacks etc.
Also contains a simple Command line game when module itself is executed
"""

import random
import components
import game_engine
import advanced_attacking

players = {}


def generate_attack(board: list[list[str | None]] = None) -> tuple[int, int]:
    """
    Generates a position to attack via specification random method
    :param board: input the board to attack so the algorithm knows how large it is. Unittests assume
    there are no arguments for generate_attack so if we get not argument assume board_size = 10
    :return: a tuple coordinate on the grid
    """

    if board:  # if argument provided for the board make the length the size
        board_size = len(board)
    else:
        board_size = 10

    # Purely random attack method
    x, y = random.randrange(0, board_size), random.randrange(0, board_size)
    return x, y


def display_ascii(board: list[list[str | None]]) -> None:
    """
    Displays a given board on the command line
    :param board: The board to display
    :return: None, it prints the result
    """

    board_size = len(board)

    print('   ' + ''.join([f'  {i + 1}   ' for i in range(board_size)]))  # Prints top numbers row

    for y in range(board_size):
        print('  ' + '-' * ((board_size * 6) + 1))  # divider on top of each row
        row = str(y + 1) + " "

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
    players['Human'] = {'board': components.initialise_board(),
                        'ships': components.create_battleships()}
    players['AI'] = {'board': components.initialise_board(),
                     'ships': components.create_battleships()}

    # Place the ships
    players['Human']['board'] = components.place_battleships(players['Human']['board'],
                                                             players['Human']['ships'],
                                                             algorithm='custom')
    players['AI']['board'] = components.place_battleships(players['AI']['board'],
                                                          players['AI']['ships'],
                                                          algorithm='random')

    while (game_engine.count_ships_remaining(players['Human']['ships']) != 0 and
           game_engine.count_ships_remaining(players['AI']['ships']) != 0):
        # Main game loop, continues as long as both players have ships (ie no one has won)
        print("-- USER'S TURN --")

        # Input validation for the coordinates, check they're in board range
        user_coords = (-1, -1)
        while not ((0 <= user_coords[0] < len(players['Human']['board']) and
                    0 <= user_coords[1] < len(players['Human']['board']))):
            user_coords = game_engine.cli_coordinates_input()
            if not ((0 <= user_coords[0] < len(players['Human']['board']) and
                     0 <= user_coords[1] < len(players['Human']['board']))):
                print("Coordinates outside of the board")

        attack_status = game_engine.attack(user_coords,
                                           players['AI']['board'],
                                           players['AI']['ships'])
        if attack_status:
            print("You got a HIT!")
        else:
            print("You got a MISS!")

        print("-- AI'S TURN --")
        ai_coords = generate_attack(players['AI']['board'])
        attack_status = game_engine.attack(ai_coords,
                                           players['Human']['board'],
                                           players['Human']['ships'])
        if attack_status:
            print("The AI got a HIT!")
        else:
            print("The AI got a MISS!")

        print(" Player's Board :")
        display_ascii(players['Human']['board'])

    if game_engine.count_ships_remaining(players['Human']['ships']) == 0:
        print(" The Human LOST! Better luck next time")
    else:
        print(" The Human WON! Well done")


if __name__ == "__main__":
    ai_opponent_game_loop()
