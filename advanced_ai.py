"""
This module just deals with the AI when its doing more advanced
 attacking rather than random guesses
"""
# import libs
import random
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
        return generate_attack_difficulty_4(enemy_dict,history)

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
    x = random.randrange(0, board_size)
    y = random.randrange(0, board_size)
    return x, y


def generate_attack_difficulty_1(board_size: int,
                                 history: list[tuple[int, int]]) -> tuple[int, int]:
    """
    Semi random guess - ie its random but it won't guess the same place twice
    :param board_size: Size of board
    :param history: list of where has been guessed before
    :return: The guess
    """
    # generate an initial random guess
    x = random.randrange(0, board_size)
    y = random.randrange(0, board_size)

    while (x, y) in history:  # Keep generating guesses until we find one not in history list
        x = random.randrange(0, board_size)
        y = random.randrange(0, board_size)

    return x, y


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

    unsunk_hits = get_unsunk_hits(enemy_dict)
    if len(unsunk_hits) != 0:
        # Do a guess with difficulty 3
        return generate_advanced_attack(3, enemy_dict, history)

    # No unsunk hits found so do a better random guess
    # This works by finding the largest ship on the board
    return 0, 0


####################
# OTHER FUNCTIONS
####################
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

    unsunk_hits = get_unsunk_hits(enemy_dict)

    line_moves = []  # will hold the moves that form a line
    for unsunk_hit in unsunk_hits:

        # Go through each position around an unsunk hit, up down etc.
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for offset in offsets:
            # if the tile on the opposite side to the offset we are currently looking at
            # is also unsunk hit, then it's likely that current offset is part of a line
            if (unsunk_hit[0] - offset[0], unsunk_hit[1] - offset[1]) in unsunk_hits:
                line_moves.append((unsunk_hit[0] + offset[0], unsunk_hit[1] + offset[1]))

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
    for y, row in enumerate(enemy_board):
        for x, cell in enumerate(row):
            if cell != enemy_original_board[y][x]:
                hit_locations.append((x, y))

    # Find the unsunk hits by doing a set difference between all hits and sunks
    unsunk_hits = list(set(hit_locations).difference(set(sunk_locations)))

    return unsunk_hits
