"""
This Module contains extra functions for extending features of the HTML/JS/Flask GUI
"""


def attack_sunk(coordinates: tuple[int, int],
                board: list[list[str | None]],
                my_guess_board : list[list[str]],
                battleships: dict[str, int]) -> tuple[str: str | None]:
    """
    This function extends the functionality of 'attack' to return the type of hit
    :param coordinates: Coordinates to check if there's a ship
    :param board: The board (list of lists) to check
    :param my_guess_board:  my guess board to check if I've guessed here yet
    :param battleships: The list of enemy ships to check
    :return: tuple of attack result ('hit', 'miss' or 'sink') then ship_name that was sunk
    """

    ship_name = board[coordinates[1]][coordinates[0]]  # Name of the ship in the position we're firing at

    is_hit = my_guess_board[coordinates[1]][coordinates[0]] == 'B'  # If it hit anything
    if is_hit:
        battleships[ship_name] -= 1

    if is_hit and battleships[ship_name] == 0:
        return 'sunk', ship_name
    elif is_hit and battleships[ship_name] > 0:
        return 'hit', ship_name
    elif my_guess_board[coordinates[1]][coordinates[0]] == 'N':
        return 'miss', None
    else:
        return 'prev_hit', None


def create_guess_board(opponent_board: list[list[str | None]]) -> list[list[str]]:
    """
    Creates the starting guess board, if an enemy ship is in that spot it's 'S' if nothing then 'N'
    :param opponent_board: The opponents starting board
    :return: Starting guess board
    """
    guess_board = []

    for opponent_row in opponent_board:
        guess_row = ['N' if i is None else 'B' for i in opponent_row]
        guess_board.append(guess_row)

    return guess_board


def update_guess_board(guess_board: list[list[str]],
                       location: tuple[int, int],
                       opponent_board: list[list[str | None]],
                       sink_result: tuple[str: str | None]) -> list[list[str]]:
    """
    This updates the guess board depending on the result of the attack_sunk function
    :param guess_board: The guess_board to update
    :param location: Where the player attacked
    :param opponent_board: The opponent board
    :param sink_result: The result of whether it was hit/sunk and the ship_name of where hit
    :return: An updated guess board
    """
    sink_status = sink_result[0]  # The status of our attack
    sink_name = sink_result[1]  # The name of the boat we hit (or None if we didn't)

    if sink_status == 'hit':
        guess_board[location[1]][location[0]] = 'H'

    elif sink_status == 'miss':
        guess_board[location[1]][location[0]] = 'M'

    elif sink_status == 'sunk':
        # If we sunk a ship find all of its tiles on the board and update them as sunk on guess map
        for y in range(len(opponent_board)):
            for x in range(len(opponent_board)):
                if opponent_board[y][x] == sink_name:
                    guess_board[y][x] = 'S'

    return guess_board
