"""
This module just deals with the AI when its doing more advanced
 attacking rather than random guesses
"""
# import libs
import random
import numpy as np
# Import battleships libs, pycharm likes it one way, terminal likes it the other
# using this try except bit here makes it work either way round
try:
    from battleships import components
except ImportError:
    import components


###############################
# MAIN ATTACK FUNCTION
###############################
def generate_advanced_attack(difficulty: int, enemy_dict: dict, history: list) -> tuple[int, int]:
    """
    Generates more advanced attack position than the attack function in the specification

    :param difficulty: 0 (easy) -> 4 (intelligent)
    :param enemy_dict: So we can get the enemy's board and original board
    :param history: Our move history, so we know where we have already guessed
    :return: A location on the board as a tuple
    """

    if (not isinstance(difficulty,int) or not isinstance(enemy_dict,dict)
            or not isinstance(history,list)):
        raise TypeError('A parameter is of incorrect type')

    try:  # Error checking for incorrect enemy_dict parameter
        enemy_board = enemy_dict['board']
    except KeyError as exc:
        raise ValueError("enemy_dict is incomplete") from exc

    if difficulty == 0:
        # Purely random attacking method (what's defined in the spec)
        return generate_attack_difficulty_0(len(enemy_board))

    if difficulty == 1:
        # Semi random - ie its random but it won't guess the same place twice
        return generate_attack_difficulty_1(len(enemy_board), history)

    if difficulty == 2:
        # This does semi intelligent guessing around unsunk hits (it chooses a random
        # location adjacent to unsunk hits) if no unsunk hits it guesses randomly
        return generate_attack_difficulty_2(enemy_dict, history)

    if difficulty == 3:
        # A bit better than difficulty 2, this tries to follow lines in the unsunk hits
        # Still does random guessing if it can't find any unsunk hits
        return generate_attack_difficulty_3(enemy_dict, history)

    if difficulty == 4:
        # If it has unsunk hits then it does the same as difficulty 3
        # But if no unsunk hits found then it does more intelligent random guessing
        return generate_attack_difficulty_4(enemy_dict, history)

    raise ValueError('Difficulty not in range 0-4!')


########################################################
# FUNCTIONS FOR EACH DIFFICULTY
########################################################
# (had to lay out like this as pylint was unhappy
# about too many return statements in main function
def generate_attack_difficulty_0(board_size: int) -> tuple[int, int]:
    """
    Purely random attacking method (what's defined in the spec)

    :param board_size: Size of the board
    :return: attack coordinate
    """
    x_co = random.randrange(0, board_size)
    y_co = random.randrange(0, board_size)
    return x_co, y_co


def generate_attack_difficulty_1(board_size: int,
                                 history: list[tuple[int, int]]) -> tuple[int, int]:
    """
    Semi random guess - ie its random but it won't guess the same place twice

    :param board_size: Size of board
    :param history: list of where has been guessed before
    :return: The guess
    """
    # generate an initial random guess
    x_co = random.randrange(0, board_size)
    y_co = random.randrange(0, board_size)

    while (x_co, y_co) in history:  # Keep generating guesses until we find one not in history list
        x_co = random.randrange(0, board_size)
        y_co = random.randrange(0, board_size)

    return x_co, y_co


def generate_attack_difficulty_2(enemy_dict: dict,
                                 history: list[tuple[int, int]]) -> tuple[int, int]:
    """
    This does semi intelligent guessing around unsunk hits (it chooses a random
    location adjacent to unsunk hits) if no unsunk hits it guesses randomly

    :param enemy_dict: So we can get the enemy's board and original board
    :param history: list of where has been guessed before
    :return: The guess
    """
    # This does semi intelligent guessing around unsunk hits (it chooses a random
    # location adjacent to unsunk hits) if no unsunk hits it guesses randomly

    try:  # Error checking for incorrect enemy_dict parameter
        enemy_board = enemy_dict['board']
    except KeyError as exc:
        raise ValueError("enemy_dict is incomplete") from exc

    unsunk_hits = get_unsunk_hits(enemy_dict)

    if len(unsunk_hits) != 0:  # guess a space around an unsunk hit randomly
        surrounding_tiles = get_surrounding_tiles(unsunk_hits, len(enemy_board))
        # Make sure this doesn't include tiles we have already guessed using sets
        surrounding_tiles = list(set(surrounding_tiles).difference(set(history)))
        return random.choice(surrounding_tiles)

    # Otherwise Guess randomly
    return generate_advanced_attack(1, enemy_dict, history)


def generate_attack_difficulty_3(enemy_dict: dict,
                                 history: list[tuple[int, int]]) -> tuple[int, int]:
    """
    A bit better than difficulty 2, this tries to follow lines in the unsunk hits
    Still does random guessing if it can't find any unsunk hits

    :param enemy_dict: So we can get the enemy's board and original board
    :param history: list of where has been guessed before
    :return: The guess location
    """
    # Error check enemy dict
    if 'board' not in enemy_dict or 'original_board' not in enemy_dict:
        raise ValueError("enemy_dict is incomplete")

    unsunk_hits = get_unsunk_hits(enemy_dict)

    if len(unsunk_hits) == 0:  # No unsunk hits so guess randomly
        return generate_advanced_attack(1, enemy_dict, history)

    return guess_line_attack(enemy_dict, history)


def generate_attack_difficulty_4(enemy_dict: dict,
                                 history: list[tuple[int, int]]) -> tuple[int, int]:
    """
    If it has unsunk hits then it does the same as difficulty 3
    But if no unsunk hits found then it does more intelligent random guessing

    :param enemy_dict: So we can get the enemy's board and original board
    :param history: list of where has been guessed before
    :return: The guess location
    """
    # error check enemy dict
    if 'board' not in enemy_dict or 'original_board' not in enemy_dict:
        raise ValueError("enemy_dict is incomplete")

    unsunk_hits = get_unsunk_hits(enemy_dict)
    if len(unsunk_hits) != 0:
        # Do a guess with difficulty 3
        return generate_advanced_attack(3, enemy_dict, history)

    # No unsunk hits found so do an intelligent blind guess

    pos = generate_intelligent_blind_guess(enemy_dict, history)
    pos = (int(pos[0]),int(pos[1]))
    # print(pos)
    return pos


####################
# OTHER FUNCTIONS
####################
def generate_intelligent_blind_guess(enemy_dict, history):
    """
    When there are no unsunk ships to guess around this algorithm gives the best place to
    try and look for a ship

    :param enemy_dict: So we can get the enemy's board and original board
    :param history: list of where has been guessed before
    :return: A location to guess
    """

    # The algorithm works by trying to put each ship in every cell on the grid
    # we then pick the cell that has the most ships potentially in it

    # enemy dict error checking
    if 'board' not in enemy_dict or 'original_board' not in enemy_dict:
        raise ValueError("enemy_dict is incomplete")

    board_size = len(enemy_dict['board'])
    enemy_ships = enemy_dict['ships']

    # Find a list of the ships we haven't hit any of yet
    ships_unseen = sorted(list({i for i in enemy_ships.values() if i != 0}), reverse=True)

    # We'll create a blank board then fill it up with our guess history
    blank_board = components.initialise_board(board_size)
    for i in history:
        blank_board[i[1]][i[0]] = 'Guessed'

    # This numpy array stores the frequencies of a ship being in a tile for each cell
    frequencies = np.zeros((board_size, board_size))

    for y_co in range(board_size):  # Go through every possible cell
        for x_co in range(board_size):

            for ship in ships_unseen:  # Go through all unseen ships

                # Test whether that ship fits into the position either vertically or horizontally
                fitted = components.try_place_ship(blank_board, 'test',
                                                   ship, (x_co, y_co), 'h')
                if fitted: # If it fits then add 1 to the frequency array
                    frequencies += np.where(np.array(fitted), 1, 0)

                fitted = components.try_place_ship(blank_board, 'test', ship,
                                                   (x_co, y_co), 'v')
                if fitted:
                    frequencies += np.where(np.array(fitted), 1, 0)

    for i in history: # remove all the guesses in our history from the frequency array
        frequencies[i[1]][i[0]] = 0

    # There may be multiple cells that share a maximum ship potential so put them in a list
    positions = list(zip(np.where(frequencies == np.max(frequencies))[1],
                         np.where(frequencies == np.max(frequencies))[0]))

    return random.choice(positions)  # and pick a random one from the list


def guess_line_attack(enemy_dict: dict, history: list[tuple[int, int]]) -> tuple[int, int]:
    """
        Generates a guess based on following lines in the unsunk hits to try and find ships

        :param enemy_dict: So we can get the enemy's board and original board
        :param history: Our move history, so we know where we have already guessed
        :return: A guess following a line if possible
        """

    # Error checking for enemy_dict
    if 'board' not in enemy_dict or 'original_board' not in enemy_dict:
        raise ValueError("enemy_dict is incomplete")

    board_size = len(enemy_dict['board'])
    unsunk_hits = get_unsunk_hits(enemy_dict)

    line_moves = []  # will hold the moves that form a line
    for unsunk_hit in unsunk_hits:

        # Go through each position around an unsunk hit, up down etc.
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for offset in offsets:
            # if the tile on the opposite side to the offset we are currently looking at
            # is also unsunk hit, then it's likely that current offset is part of a line
            if (unsunk_hit[0] - offset[0], unsunk_hit[1] - offset[1]) in unsunk_hits:
                potential_move = (unsunk_hit[0] + offset[0], unsunk_hit[1] + offset[1])
                if board_size > potential_move[0] >= 0 and board_size > potential_move[1] >= 0:
                    line_moves.append(potential_move)

    # just make sure line_moves doesn't contain anywhere we have guessed already
    line_moves = list(set(line_moves).difference(set(history)))

    if len(line_moves) == 0:
        # Found no moves that form a line so just pick a move surrounding an unsunk hit
        # basically difficulty 2
        return generate_advanced_attack(2, enemy_dict, history)

    # We have found at least 1 line move so choose one from the list
    return random.choice(line_moves)


def get_surrounding_tiles(search_tiles: list[tuple[int, int]],
                          board_size: int) -> list[tuple[int, int]]:
    """
    Gives a list of the tiles surrounding the tiles given by 'search_tiles' parameter
    primarily used for finding tiles around unsunk hits

    :param search_tiles: The tiles to look around
    :param board_size: The size of the board
    :return: The list of surrounding tiles
    """
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    surrounding_tiles = []

    for tile in search_tiles:
        # For each tile in search_list go through the tiles next to it
        for offset in offsets:
            # check if offset tile is within board
            potential_tile = (tile[0] + offset[0], tile[1] + offset[1])
            if board_size > potential_tile[0] >= 0 and board_size > potential_tile[1] >= 0:
                surrounding_tiles.append(potential_tile)

    return surrounding_tiles


def get_unsunk_hits(enemy_dict: dict) -> list[tuple[int, int]]:
    """
    Find all the cells in the board that have been hit but not sunk

    :param enemy_dict: So we can get the enemy's board and original board
    :return: The list of unsunk hit locations
    """
    # Check enemy dict set up correctly
    try:  # Error checking for incorrect enemy_dict parameter
        enemy_board = enemy_dict['board']
        enemy_original_board = enemy_dict['original_board']

    except KeyError as exc:
        raise ValueError("enemy_dict is incomplete") from exc

    sunk_locations = components.get_sunken_ships(enemy_dict)

    # Find all the places in the board that have been hit (difference
    # between original board and current board)
    hit_locations = []
    for y_co, row in enumerate(enemy_board):
        for x_co, cell in enumerate(row):
            if cell != enemy_original_board[y_co][x_co]:
                hit_locations.append((x_co, y_co))

    # Find the unsunk hits by doing a set difference between all hits and sunks
    unsunk_hits = list(set(hit_locations).difference(set(sunk_locations)))

    return unsunk_hits
