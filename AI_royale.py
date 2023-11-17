"""
This module is used for testing different versions of the AI against each other
Also good for brute force testing to see if errors come up
"""

import components
import game_engine
import mp_game_engine as mpg
import gui_extensions
import storm_engine

def ai_opponent_game_loop(mode1: int, mode2: int) -> str:
    """
    Plays a command line game of battleships against an AI
    :param mode1: The difficulty mode for AI1
    :param mode2: The difficulty mode for AI2
    :return: the winner of the match either 'AI1' or 'AI2'
    """

    storm_direction = (0, 0)  # In case you want to add a storm in

    # Initialise the AI's as players in a dictionary
    players = {'AI2': {'board': components.initialise_board(), 'ships': components.create_battleships()},
               'AI': {'board': components.initialise_board(), 'ships': components.create_battleships()}}

    # Place the ships randomly
    players['AI2']['board'] = components.place_battleships(players['AI2']['board'],
                                                           players['AI2']['ships'],
                                                           placement_method='random')
    players['AI']['board'] = components.place_battleships(players['AI']['board'],
                                                          players['AI']['ships'],
                                                          placement_method='random')

    # Set up their guess_boards
    players['AI2']['guess_board'] = gui_extensions.create_guess_board(players['AI']['board'])
    players['AI']['guess_board'] = gui_extensions.create_guess_board(players['AI2']['board'])

    while (game_engine.count_ships_remaining(players['AI2']['ships']) != 0 and
           game_engine.count_ships_remaining(players['AI']['ships']) != 0):
        # Main game loop, continues as long as both AIs have ships (ie no one has won)

        # AI2 makes its attack
        ai_coords = mpg.generate_attack_ext(players['AI2']['board'],
                                            difficulty=mode2,
                                            my_guess_board=players['AI2']['guess_board'])
        attack_status = gui_extensions.attack_sunk(ai_coords,
                                                   players['AI']['board'],
                                                   players['AI2']['guess_board'],
                                                   players['AI']['ships'])
        players['AI2']['guess_board'] = gui_extensions.update_guess_board(players['AI2']['guess_board'],
                                                                          ai_coords,
                                                                          players['AI']['board'],
                                                                          attack_status)

        # AI1 makes its attack
        ai_coords = mpg.generate_attack_ext(players['AI']['board'],
                                            difficulty=mode1,
                                            my_guess_board=players['AI']['guess_board'])
        attack_status = gui_extensions.attack_sunk(ai_coords,
                                                   players['AI2']['board'],
                                                   players['AI']['guess_board'],
                                                   players['AI2']['ships'])
        players['AI']['guess_board'] = gui_extensions.update_guess_board(players['AI']['guess_board'],
                                                                         ai_coords,
                                                                         players['AI2']['board'],
                                                                         attack_status)
        players['AI']['guess_board'] = storm_engine.shift(players['AI']['guess_board'], storm_direction)
        players['AI2']['board'] = storm_engine.shift(players['AI2']['board'], storm_direction)
        players['AI2']['guess_board'] = storm_engine.shift(players['AI2']['guess_board'], storm_direction)
        players['AI']['board'] = storm_engine.shift(players['AI']['board'], storm_direction)


    # Check who won and return the winner
    if game_engine.count_ships_remaining(players['AI2']['ships']) == 0:
        return 'AI1'
    else:
        return 'AI2'


if __name__ == "__main__":

    # Scores of the AIs
    AI1 = 0
    AI2 = 0
    total = 2000

    ai1_difficulty = 3
    ai2_difficulty = 4

    for i in range(total): # Run it a good number of times and tally who won
        result = ai_opponent_game_loop(ai1_difficulty, ai2_difficulty)
        if result == 'AI1':
            AI1 += 1
        else:
            AI2 += 1

    # Output winner info
    print(f'AI1 won {100 * AI1 / total}% matches \n AI2 won {100 * AI2 / total}% of matches')
