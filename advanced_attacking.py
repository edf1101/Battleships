"""
This module just deals with the AI when its doing more advanced
 attacking rather than random guesses
"""

import random
import components
import mp_game_engine


def generate_attack_challenging(my_guess_board: list[list[str]],
                                min_ship_size: int,
                                difficulty: int) -> tuple[int, int]:
    """
    This generates a more intelligent (not purely random) guess
    :param my_guess_board: The guess board, so we know where we have guessed prior
     and where has/ hasn't been sunk
    :param min_ship_size: The smallest ship on the board
    :param difficulty: The attack method difficulty, given this is the intelligent
     AI algorithm its (2-4)
    :return: A tuple location of where to guess
    """

    # Check parameter types
    if not isinstance(min_ship_size,int) or not isinstance(difficulty,int) or not isinstance(my_guess_board, list):
        raise TypeError('parameters incorrect type')

    for row in my_guess_board:
        if not isinstance(row,list):
            raise TypeError('not all rows of guess board are lists')

    # First going to find the places we have hit but not sunk by iterating through guess board
    unsunk_hits = []
    for y, row in enumerate(my_guess_board):
        for x in range(len(my_guess_board)):
            guess_value = row[x]
            if guess_value == 'H':
                unsunk_hits.append((x, y))

    if len(unsunk_hits) == 0:  # Haven't got any unsunk hits, so we need to guess

        if difficulty == 2:  # If difficulty 2 generate a random point if we have no hits to go off
            # Reuse the attack function but set it to a low difficulty to generate random point
            x, y = mp_game_engine.generate_attack_ext(my_guess_board,
                                                      difficulty=1,
                                                      my_guess_board=my_guess_board)
            return x, y

        # If difficulty 3 or 4 generate a smart random point if we have no hits to go off
        if difficulty in [3, 4]:
            x, y = generate_blind_point(my_guess_board, min_ship_size)
            return x, y

        raise ValueError(f'difficulty parameter invalid cant be {difficulty}')

    # If the difficulty parameter is 2 or 3 make a semi-intelligent unseen hits guess
    if difficulty in [2, 3]:
        x, y = calculate_unsunk_attack(my_guess_board, unsunk_hits, intelligent=False)
        return x, y

    if difficulty == 4:  # If the difficulty parameter 4 make an intelligent unseen hits guess
        x, y = calculate_unsunk_attack(my_guess_board, unsunk_hits, intelligent=True)
        return x, y

    # error raised if someone uses an invalid method parameter
    raise ValueError(f'difficulty parameter invalid cant be {difficulty}')


def calculate_unsunk_attack(my_guess_board: list[list[str]],
                            unsunk_hits: list[tuple[int, int]],
                            intelligent: bool = True) -> tuple[int, int]:
    """
    When we have hit (but not sunk) positions on the board we should target around
     them this function does that
    :param my_guess_board: The guess board, so we know where we have guessed prior
     and where has/ hasn't been sunk
    :param unsunk_hits: Holds where we know there's been a hit, but not a sink
    :param intelligent: True for the best result, or False is a little less accurate
    :return: The location where to fire
    """

    # For each unsunk move add its neighbours to the potential moves dictionary
    potential_moves = {}
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for unsunk in unsunk_hits:

        # For each unsunk hit add the surrounding tiles to the dictionary
        for offset in offsets:

            # Get the combination of position + offset
            trial_position = (offset[0] + unsunk[0], offset[1] + unsunk[1])

            # If it's outside the board ignore it
            if not components.in_board(trial_position, my_guess_board):
                continue

            been_guessed = not (my_guess_board[trial_position[1]][trial_position[0]] == 'N' or
                                my_guess_board[trial_position[1]][trial_position[0]] == 'B')

            if not been_guessed:  # As long as they haven't been guessed add to dict
                if unsunk in potential_moves:
                    potential_moves[unsunk].append(trial_position)
                else:
                    potential_moves[unsunk] = [trial_position]

    if not intelligent:
        # Choose a random option from all the potential moves

        # Combine the dictionary values into a list
        all_moves = sum(list(potential_moves.values()), [])

        if len(all_moves) != 0:
            return random.choice(all_moves)  # Pick a random one from the potential move list

        # If we can't find a move then use a random one instead from existing function
        return mp_game_engine.generate_attack_ext(my_guess_board, difficulty=1,
                                                  my_guess_board=my_guess_board)

    if intelligent:
        return unsunk_pick_line(potential_moves, unsunk_hits, my_guess_board)

    raise SyntaxError(f'{intelligent} is not a valid argument for intelligent param')


def unsunk_pick_line(potential_moves: dict,
                     unsunk_hits: list[tuple[int, int]],
                     my_guess_board: list[list[str]]) -> tuple[int, int]:
    """
    It predicts where ships might be given lines formed by unsunk ships
    :param potential_moves: The Dictionary of potential moves around each unsunk ship
    :param unsunk_hits: The list of unsunk hits on the board
    :param my_guess_board: My guess board
    :return: A position to guess
    """
    # With this mode it trys to follow lines where previous hits have been

    great_moves = []  # potential moves that follow in a line

    for origin, move_for_tile in potential_moves.items():

        for potential in move_for_tile:  # Go through all the potential moves

            offset = (potential[0] - origin[0], potential[1] - origin[1])

            # If the move to the in the opposite direction of its offset
            # is a hit then there's a strong chance this next move will be a hit too
            if (origin[0] - offset[0], origin[1] - offset[1]) in unsunk_hits:
                great_moves.append(potential)

    # If there aren't any moves that form an obvious line choose any potential move
    if len(great_moves) == 0:

        # Combine the dictionary values into a list
        all_moves = sum(list(potential_moves.values()), [])

        if len(all_moves) != 0:
            return random.choice(all_moves)  # Pick a random one from the potential move list

        # If we can't find a move then use a random one instead from existing function
        return mp_game_engine.generate_attack_ext(my_guess_board, difficulty=1,
                                                  my_guess_board=my_guess_board)

    # If there are some moves that form a line pick one of them
    return random.choice(great_moves)


def calculate_min_ship_size(board: list[list[str | None]]) -> int:
    """
    Calculates the size of the smallest ship on the board just from the guess board
    :param board: Their original board containing ship names that gets passed in
    :return: The size of the smallest ship
    """

    # Goes through each cell and increments the ship's count in a dictionary
    ships_counts = {}
    for y, _ in enumerate(board):
        for x in range(len(board)):
            cell = board[y][x]
            if cell and cell in ships_counts:
                ships_counts[cell] += 1
            elif cell:
                ships_counts[cell] = 1

    return min(ships_counts.values())  # returns the minimum from the dictionary values


def generate_blind_point(my_guess_board: list[list[str]], min_ship_size: int) -> tuple[int, int]:
    """
    If there are no unsunk hits on the board this function will return the best place to guess
    :param my_guess_board: The guess board, so we know where we have guessed prior and
    where has/ hasn't been sunk
    :param min_ship_size: The smallest ship on the board
    :return: A tuple location in the list of lists
    """

    # First generate a list of points we may want to guess
    # Generated in a semi-checkerboard pattern so if we guess them all it's impossible to miss
    checkerboard_points_guessed = []
    checkerboard_points_not_guessed = []

    for y, row in enumerate(my_guess_board):
        for x in range(0, int((len(my_guess_board) - 1 - (y % min_ship_size)) / min_ship_size) + 1):
            x = (x * min_ship_size) + (y % min_ship_size)
            if row[x] == 'N' or row[x] == 'B':  # Haven't guessed before
                checkerboard_points_not_guessed.append((x, y))
            else:
                checkerboard_points_guessed.append((x, y))

    # To judge the best place to blind guess use 3 metrics then combine them and take the best
    metrics = ([], [], [])
    # Metric 0 is the distance to already guessed positions (higher better)
    # Metric 1 isThe distance to the positions not guessed yet (lower better)
    # Metric 2 for how many guessed tiles nearby

    for point1 in checkerboard_points_not_guessed:

        # Get the distance to already guessed positions, penalise this
        # so we don't get too clumped points
        metric = 0
        for point2 in checkerboard_points_guessed:
            metric += pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2)
        metrics[0].append(metric)

        # Get the distance to not guessed positions, encourage this
        # so we space out the points
        metric = 0
        for point2 in checkerboard_points_not_guessed:
            metric += pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2)
        metrics[1].append(metric)

        # If the distance to a guessed tile is less than half the board away
        # add 1 to the metric, This prevents grouping
        metric = 0
        for point2 in checkerboard_points_guessed:
            if ((pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))
                    < len(my_guess_board) / 2):
                metric += 1
        metrics[2].append(metric)

    # Add the scores in the 3 metric then whichever tile has the lowest position overall is the best
    combined_metric = []
    for metric_1, metric_2, metric_3 in zip(metrics[0],
                                            metrics[1],
                                            metrics[2]):

        # Combine the metrics and add it to a combined metrics list
        combined_metric.append((sorted(metrics[0], reverse=True).index(metric_1) +
                                sorted(metrics[1]).index(metric_2) +
                                sorted(metrics[2]).index(metric_3)))

    if len(combined_metric) == 0:
        # If we can't find a move then use a random one instead from existing function
        return mp_game_engine.generate_attack_ext(my_guess_board, difficulty=1,
                                                  my_guess_board=my_guess_board)

    # The best tile will be the one with the lowest tile metric
    # Get the index of this tile in the checkerboard list and return it
    return checkerboard_points_not_guessed[combined_metric.index(min(combined_metric))]
