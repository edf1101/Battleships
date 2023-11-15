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

        valid_input = x.isnumeric() and y.isnumeric() and int(x) > 0 and int(y) > 0

        if not valid_input:
            print("INVALID ENTRY - values must be positive and integers")

    x, y = int(x)-1, int(y)-1
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

        # Input validation for the coordinates, check they're in board range
        coordinates = (-1, -1)
        while not (0 <= coordinates[0] < len(board) and 0 <= coordinates[1] < len(board)):
            coordinates = cli_coordinates_input()
            while not (0 <= coordinates[0] < len(board) and 0 <= coordinates[1] < len(board)):
                coordinates = cli_coordinates_input()
                if not (0 <= coordinates[0] < len(board) and 0 <= coordinates[1] < len(board)):
                    print("Coordinates outside of the board")

        attack_status = attack(coordinates, board, ships)
        if attack_status:
            print("You got a HIT!")
        else:
            print("You got a MISS!")

    print("---------------  GAME OVER --------------- ")
    print("#### THANK YOU FOR PLAYING BATTLESHIPS ###")


if __name__ == "__main__":
    simple_game_loop()
