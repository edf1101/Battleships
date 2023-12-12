"""
This module runs unit tests for game_engine.py file
Authors:
Student 130003140  (Additional Functionality Tests)
Matt Collison (Example Unit Tests provided)
"""

import importlib
import pytest
import test_helper_functions as thf

testReport = thf.TestReport("test_report.txt")


@pytest.mark.depends()
def test_game_engine_exists() -> None:
    """
    Test if the game_engine module exists.
    """
    try:
        importlib.import_module('battleships.game_engine')
    except ImportError:
        testReport.add_message("game_engine module does not exist in your solution.")
        pytest.fail("game_engine module does not exist")


############
# Test Attack Function
############
@pytest.mark.depends(on=["test_game_engine_exists"])
def test_attack_exists() -> None:
    """
    Test if the attack function exists.
    """
    try:
        game_engine = importlib.import_module('battleships.game_engine')
        assert hasattr(game_engine, 'attack'), "attack function does not exist"
    except AssertionError:
        testReport.add_message("attack function does not exist in your solution.")
        pytest.fail("attack function does not exist")


@pytest.mark.depends(on=["test_game_engine_exists"])
def test_attack_arguments() -> None:
    """
    Test if the attack function accepts a tuple, a list, and a dictionary argument.
    """
    try:
        components = importlib.import_module('battleships.components')
        game_engine = importlib.import_module('battleships.game_engine')
        coordinates = (1, 1)
        board = components.initialise_board(10)
        battleships = components.create_battleships("battleships.txt")
        game_engine.attack(coordinates, board, battleships)
    except TypeError:
        testReport.add_message("attack function does not accept a tuple, a list, and a dictionary argument")
        pytest.fail("attack function does not accept a tuple, a list, and a dictionary argument")
    except Exception:
        testReport.add_message("test_attack_arguments failed as one of the functions place_battleships, "
                               "initialise_board or create_battleships or attack"
                               " threw an unexpected error. ("
                               "Crashed before test completed). Check the test output window for deatils")
        pytest.fail("test_attack_arguments failed as one of the functions place_battleships, "
                    "initialise_board or create_battleships or attack"
                    " threw an unexpected error. ("
                    "Crashed before test completed).")


@pytest.mark.depends(on=["test_game_engine_exists"])
def test_attack_arguments_invalid() -> None:
    try:
        game_engine = importlib.import_module('battleships.game_engine')

        valid_coordinates = (1, 2)
        valid_board = [[None, None, 'Ship1', None],
                       [None, None, 'Ship1', None],
                       [None, None, 'Ship1', None],
                       [None, None, None, None]]
        valid_ships = {'ship1': 3}

        # Test giving board parameter as a string not a list of lists
        with pytest.raises(TypeError):
            game_engine.attack(valid_coordinates, 'board', valid_ships)

        # Test giving board parameter as a list where one item in it isn't a list
        invalid_board = [[None, None, 'Ship1', None],
                         [None, None, 'Ship1', None],
                         [None, None, 'Ship1', None],
                         'bad']
        with pytest.raises(TypeError):
            game_engine.attack(valid_coordinates, invalid_board, valid_ships)
        # Test giving board parameter as a list where one item in the list of lists
        # isn't a str or None
        invalid_board = [[None, None, 'Ship1', None],
                         [None, None, 'Ship1', None],
                         [None, None, 'Ship1', None],
                         [None, 3, None, None]]
        with pytest.raises(TypeError):
            game_engine.attack(valid_coordinates, invalid_board, valid_ships)

        # Test invalid coordinates should be tuple[int,int]
        with pytest.raises(TypeError):
            game_engine.attack((1, 'b'), valid_board, valid_ships)
        with pytest.raises(TypeError):
            game_engine.attack('c', valid_board, valid_ships)
        with pytest.raises(ValueError):
            game_engine.attack((1, 1, 2), valid_board, valid_ships)
        # test coordinate out of board
        with pytest.raises(ValueError):
            game_engine.attack((1, 200), valid_board, valid_ships)

        # Test invalid ship dicts
        invalid_ships = {1: 'b'}
        with pytest.raises(TypeError):
            game_engine.attack(valid_coordinates, valid_board, invalid_ships)
        invalid_ships = {}  # test with empty dict
        with pytest.raises(ValueError):
            game_engine.attack(valid_coordinates, valid_board, invalid_ships)

    except AssertionError as msg:
        testReport.add_message('test_attack_arguments_invalid failed')
        pytest.fail(msg)


@pytest.mark.depends(on=["test_game_engine_exists"])
def test_attack_functionality() -> None:
    try:
        game_engine = importlib.import_module('battleships.game_engine')

        valid_coordinates = (1, 2)
        valid_board = [[None, None, 'Ship1', None],
                       [None, None, 'Ship1', None],
                       [None, None, 'Ship1', None],
                       [None, None, None, None]]
        valid_ships = {'Ship1': 3}

        # Test hitting an object
        test_output = game_engine.attack((2, 0), valid_board, valid_ships)
        expected_output = True
        assert test_output == expected_output
        # check ship has be decremented
        assert valid_ships['Ship1'] == 2

        # Test missing an object
        test_output = game_engine.attack((1, 0), valid_board, valid_ships)
        expected_output = False
        assert test_output == expected_output
        # check ship hasn't been decremented
        assert valid_ships['Ship1'] == 2

    except AssertionError as msg:
        testReport.add_message('test_attack_arguments_invalid failed')
        pytest.fail(msg)


########################################
# Test count_ships_remaining
########################################
@pytest.mark.depends(on=["test_game_engine_exists"])
def test_count_ships_remaining_invalid() -> None:
    try:
        game_engine = importlib.import_module('battleships.game_engine')

        # Test invalid ship dicts
        invalid_ships = {1: 'b'}
        with pytest.raises(TypeError):
            game_engine.count_ships_remaining(invalid_ships)
        invalid_ships = {}  # test with empty dict
        with pytest.raises(ValueError):
            game_engine.count_ships_remaining(invalid_ships)

    except AssertionError as msg:
        testReport.add_message('test_count_ships_remaining_invalid failed')
        pytest.fail(msg)


@pytest.mark.depends(on=["test_game_engine_exists"])
def test_count_ships_remaining_functionality() -> None:
    try:
        game_engine = importlib.import_module('battleships.game_engine')

        valid_ships = {'ship2': 2, 'ship3': 0, 'ship5': 3}
        expected_output = 5
        test_output = game_engine.count_ships_remaining(valid_ships)
        assert expected_output == test_output

    except AssertionError as msg:
        testReport.add_message('test_count_ships_remaining_functionality failed')
        pytest.fail(msg)


@pytest.mark.depends(on=["test_game_engine_exists"])
def test_count_ships_remaining_returns_int() -> None:
    try:
        game_engine = importlib.import_module('battleships.game_engine')

        valid_ships = {'ship2': 2, 'ship3': 0, 'ship5': 2}
        test_output = game_engine.count_ships_remaining(valid_ships)

        # Check return type is int
        assert isinstance(test_output, int)

    except AssertionError as msg:
        testReport.add_message('test_count_ships_remaining_returns_int failed')
        pytest.fail(msg)


########################################################
# Basic tests for remaining funcs
# Cant test properly as they require user input
########################################################
@pytest.mark.depends(on=["test_game_engine_exists"])
def test_cli_coordinates_input_exists():
    """
    Test if the cli_coordinates_input function exists.
    """
    try:
        game_engine = importlib.import_module('game_engine')
        assert hasattr(game_engine, 'cli_coordinates_input'), "cli_coordinates_input function does not exist"
    except AssertionError:
        testReport.add_message("cli_coordinates_input function does not exist in your solution.")
        pytest.fail("cli_coordinates_input function does not exist")


@pytest.mark.depends(on=["test_game_engine_exists"])
def test_simple_game_loop_exists():
    """
    Test if the simple_game_loop function exists.
    """
    try:
        game_engine = importlib.import_module('game_engine')
        assert hasattr(game_engine, 'simple_game_loop'), "simple_game_loop function does not exist"
    except AssertionError:
        testReport.add_message("simple_game_loop function does not exist in your solution.")
        pytest.fail("simple_game_loop function does not exist")
