"""
This script is for comparing different difficulties of AI over many games
"""

# Import gameplay libs
from copy import deepcopy
import numpy as np

# Import battleships libs, pycharm likes it one way, terminal likes it the other
# using this try except bit here makes it work either way round
try:
    from battleships import game_engine as ge
    from battleships import components
    from battleships import advanced_ai as ai
except ImportError:
    import game_engine as ge
    import components
    import advanced_ai as ai


def ai_loop(ai_mode_1: int, ai_mode_2: int) -> tuple[str, int]:
    """
    Runs a single game between two AIs

    :param ai_mode_1: the difficulty of AI 1
    :param ai_mode_2: the difficulty of AI 2
    :return: 'AI1' if AI1 won or 'AI2' if AI2 won
    """

    if not isinstance(ai_mode_1, int) or not isinstance(ai_mode_2, int):
        raise TypeError('parameters not ints')

    board_size = 10
    moves = 0  # Keep track of how many moves its taken

    players = {'AI2': {'board': components.initialise_board(board_size),
                       'ships': components.create_battleships(),
                       'history': []},
               'AI': {'board': components.initialise_board(board_size),
                      'ships': components.create_battleships(),
                      'history': []}}

    players['AI']['board'] = components.place_battleships(players['AI']['board'],
                                                          players['AI']['ships'],
                                                          algorithm='random')
    # Now AI1 has made its board lets save the original board so we can keep track
    # of what's sunk and where
    players['AI']['original_board'] = deepcopy(players['AI']['board'])

    players['AI2']['board'] = components.place_battleships(players['AI2']['board'],
                                                           players['AI2']['ships'],
                                                           algorithm='random')
    # Now AI2 has made its board lets save the original board so we can keep track
    # of what's sunk and where
    players['AI2']['original_board'] = deepcopy(players['AI2']['board'])

    finished = False

    while not finished:
        moves += 1
        # AI1 can attack
        ai_coords = ai.generate_advanced_attack(ai_mode_1,
                                                players['AI2'],
                                                players['AI']['history'])
        ge.attack(ai_coords, players['AI2']['board'],
                  players['AI2']['ships'])
        players['AI']['history'].append(ai_coords)

        # AI2 can attack now
        ai_coords = ai.generate_advanced_attack(ai_mode_2,
                                                players['AI'],
                                                players['AI2']['history'])
        ge.attack(ai_coords, players['AI']['board'],
                  players['AI']['ships'])
        players['AI2']['history'].append(ai_coords)

        # Check if finished
        finished = (ge.count_ships_remaining(players['AI2']['ships']) == 0 or
                    ge.count_ships_remaining(players['AI']['ships']) == 0)

    ai_won = ge.count_ships_remaining(players['AI2']['ships']) == 0
    # Return who won and how many moves it took
    return 'AI1' if ai_won else 'AI2', moves


def run_trials(ai1_mode: int, ai2_mode: int, trials: int = 1000) -> None:
    """
    Runs a number of games against the AI and prints the result

    :param ai1_mode: the difficulty of AI 1
    :param ai2_mode: the difficulty of AI 2
    :param trials: How many trials to run
    :return: None
    """

    # Keeps track of how many times a1 or a2 win
    ai1_score = 0
    ai2_score = 0

    # Keeps track of when ai1 / ai2 does win how many moves it look
    ai1_completion_moves = []
    ai2_completion_moves = []

    # Run it 'trials' number of times
    for i in range(1, trials):
        winner, moves = ai_loop(ai1_mode, ai2_mode)
        if winner == 'AI1':
            ai1_score += 1
            ai1_completion_moves.append(moves)
        else:
            ai2_score += 1
            ai2_completion_moves.append(moves)

        print(f'Game {i}  {winner} won')

    print(f'AI1 won {round(100 * ai1_score / (trials - 1), 2)}%'
          f'  AI2 won {round(100 * ai2_score / (trials - 1), 2)}% ')

    print(f'AI1 finished in mean = {round(np.average(ai1_completion_moves), 2)} moves'
          f'   std = {round(np.std(ai1_completion_moves), 2)}'
          f'   n = {trials}')

    print(f'AI2 finished in mean = {round(np.average(ai2_completion_moves), 2)} moves'
          f'   std = {round(np.std(ai2_completion_moves), 2)}'
          f'   n = {trials}')


if __name__ == '__main__':
    run_trials(ai1_mode=0, ai2_mode=0, trials=1000)
