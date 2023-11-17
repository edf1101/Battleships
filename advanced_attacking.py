"""
This module just deals with the AI when its doing more advanced attacking rather than random guesswork
"""

import random
import components
import mp_game_engine


def generate_attack_challenging(my_guess_board: list[list[str]],
                                min_ship_size: int,
                                difficulty: int) -> tuple[int, int]:
    """
    This generates a more intelligent (not purely random) guess
    :param my_guess_board: The guess board, so we know where we have guessed prior and where has/ hasn't been sunk
    :param min_ship_size: The smallest ship on the board
    :param difficulty: The attack method difficulty, given this is the intelligent AI algorithm its (2-4)
    :return: A tuple location of where to guess
    """

    unsunk_hits = []  # First going to find the places we have hit but not sunk by iterating through guess board
    for y in range(len(my_guess_board)):
        for x in range(len(my_guess_board)):
            guess_value = my_guess_board[y][x]
            if guess_value == 'H':
                unsunk_hits.append((x, y))

    if len(unsunk_hits) == 0:  # Haven't got any unsunk hits, so we need to guess

        if difficulty == 2:  # If difficulty 2 generate a random point if we have no hits to go off
            # Reuse the attack function but set it to a low difficulty to generate random point
            x, y = mp_game_engine.generate_attack_ext(my_guess_board, difficulty=1, my_guess_board=my_guess_board)
            return x, y

        elif difficulty in [3, 4]:  # If difficulty 3 or 4 generate a smart random point if we have no hits to go off
            x, y = generate_blind_point(my_guess_board, min_ship_size)
            return x, y

        else:
            raise SyntaxError(f'difficulty parameter invalid cant be {difficulty}')

    elif difficulty in [2, 3]:  # If the difficulty parameter is 2 or 3 make a semi-intelligent unseen hits guess
        x, y = calculate_unsunk_attack(my_guess_board, unsunk_hits, intelligent=False)
        return x, y

    elif difficulty == 4:  # If the difficulty parameter 4 make an intelligent unseen hits guess
        x, y = calculate_unsunk_attack(my_guess_board, unsunk_hits, intelligent=True)
        return x, y

    else:  # error raised if someone uses an invalid method parameter
        raise SyntaxError(f'difficulty parameter invalid cant be {difficulty}')


def calculate_unsunk_attack(my_guess_board: list[list[str]],
                            unsunk_hits: list[tuple[int, int]],
                            intelligent: bool = True) -> tuple[int, int]:
    """
    When we have hit (but not sunk) positions on the board we should target around them this function does that
    :param my_guess_board: The guess board, so we know where we have guessed prior and where has/ hasn't been sunk
    :param unsunk_hits: Holds where we know there's been a hit, but not a sink
    :param intelligent: True for the best result, or False is a little less accurate
    :return: The location where to fire
    """

    # For each unsunk move add its neighbours to the potential moves list
    potential_moves = {}
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for unsunk in unsunk_hits:
        for offset in offsets:

            trial_position = (offset[0] + unsunk[0], offset[1] + unsunk[1])  # Get the combination of position + offset

            if not components.in_board(trial_position, my_guess_board):  # If it's outside the board ignore it
                continue

            been_guessed = not (my_guess_board[trial_position[1]][trial_position[0]] == 'N' or
                                my_guess_board[trial_position[1]][trial_position[0]] == 'B')

            if not been_guessed:
                if unsunk in potential_moves:
                    potential_moves[unsunk].append(trial_position)
                else:
                    potential_moves[unsunk] = [trial_position]

    if not intelligent:
        # Choose a random option from all the potential moves

        all_moves = sum([i for i in potential_moves.values()], [])  # Combine the dictionary values into a list
        return random.choice(all_moves)  # Pick a random one

    elif intelligent:
        # With this mode it trys to follow lines where previous hits have been

        great_moves = []  # potential moves that follow in a line

        for origin, move_for_tile in potential_moves.items():

            for potential in move_for_tile:  # Go through all the potential moves

                offset = (potential[0] - origin[0], potential[1] - origin[1])

                # If the move to the in the opposite direction of its offset is a hit then there's a strong chance this
                # next move will be a hit too
                if (origin[0] - offset[0], origin[1] - offset[1]) in unsunk_hits:
                    great_moves.append(potential)

        if len(great_moves) == 0:  # If there aren't any moves that form an obvious line choose any potential move

            all_moves = sum([i for i in potential_moves.values()], [])  # Combine the dictionary values into a list
            return random.choice(all_moves)  # Pick a random one

        else:
            return random.choice(great_moves)  # If there are some moves that form a line pick one of them

    else:
        raise SyntaxError(f'You used a wrong argument, {intelligent} is not a valid argument for intelligent param')


def calculate_min_ship_size(board: list[list[str | None]]) -> int:
    """
    Calculates the size of the smallest ship on the board just from the guess board
    :param board: Their original board containing ship names that gets passed in
    :return: The size of the smallest ship
    """

    # Goes through each cell and increments the ship's count in a dictionary
    ships_counts = {}
    for y in range(len(board)):
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
    :param my_guess_board: The guess board, so we know where we have guessed prior and where has/ hasn't been sunk
    :param min_ship_size: The smallest ship on the board
    :return: A tuple location in the list of lists
    """

    # First generate a list of points we may want to guess
    # Generated in a semi-checkerboard pattern so if we guess them all it's impossible to miss
    checkerboard_points_guessed = []
    checkerboard_points_not_guessed = []
    for y in range(len(my_guess_board)):
        for x in range(0, int((len(my_guess_board) - 1 - (y % min_ship_size)) / min_ship_size) + 1):
            x = (x * min_ship_size) + (y % min_ship_size)
            if my_guess_board[y][x] == 'N' or my_guess_board[y][x] == 'B':  # Haven't guessed before
                checkerboard_points_not_guessed.append((x, y))
            else:
                checkerboard_points_guessed.append((x, y))

    # To judge the best place to blind guess we will use 3 metrics then combine them and take the best
    dist_to_guess_metric = []  # Metric of distance to already guessed positions (higher better)
    dist_to_unguessed = []  # The distance to the positions not guessed yet (lower better)
    guessed_nearby = []  # Metric of how many guessed tiles nearby

    for point1 in checkerboard_points_not_guessed:

        metric = 0
        for point2 in checkerboard_points_guessed:
            dist = pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2)
            metric += dist
        dist_to_guess_metric.append(metric)

        metric = 0
        for point2 in checkerboard_points_not_guessed:
            dist = pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2)
            metric += dist
        dist_to_unguessed.append(metric)

        metric = 0
        for point2 in checkerboard_points_guessed:
            dist = pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2)
            if dist < len(my_guess_board) / 2:
                metric += 1
        guessed_nearby.append(metric)

    # Add all the scores in the 3 metric up then whichever tile has the lowest position overall is the best
    combined_metric = []
    for metric_1, metric_2, metric_3 in zip(dist_to_guess_metric, dist_to_unguessed, guessed_nearby):
        score = (sorted(dist_to_guess_metric, reverse=True).index(metric_1) +
                 sorted(dist_to_unguessed).index(metric_2) +
                 sorted(guessed_nearby).index(metric_3))
        combined_metric.append(score)

    if len(combined_metric) == 0:
        raise NotImplementedError("This shouldn't be called unless I have made an error coding")

    # Get the index of the tile with the best metric then return the tile location
    best_tile_index = combined_metric.index(min(combined_metric))

    return checkerboard_points_not_guessed[best_tile_index]
