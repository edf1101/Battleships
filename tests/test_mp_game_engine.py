"""
This module runs unit tests for mp_game_engine.py file
Authors:
Student 130003140  (Additional Functionality Tests)
Matt Collison (Example Unit Tests provided)
"""

import importlib
import pytest
import test_helper_functions as thf

testReport = thf.TestReport("test_report.txt")


@pytest.mark.depends()
def test_mp_game_engine_exists():
    """
    Test if the mp_game_engine module exists.
    """
    try:
        importlib.import_module('battleships.mp_game_engine')
    except ImportError:
        testReport.add_message("mp_game_engine module does not exist in your solution.")
        pytest.fail("mp_game_engine module does not exist")


####################################
# Test generate_attack Function
####################################
@pytest.mark.depends(on=["test_mp_game_engine_exists"])
def test_generate_attack_exists():
    """
    Test if the generate_attack function exists.
    """
    try:
        mp_game_engine = importlib.import_module('battleships.mp_game_engine')
        assert hasattr(mp_game_engine, 'generate_attack'), "generate_attack function does not exist"
    except AssertionError:
        testReport.add_message("generate_attack function does not exist in your solution.")
        pytest.fail("generate_attack function does not exist")


@pytest.mark.depends(on=["test_mp_game_engine_exists"])
def test_generate_attack_return_type():
    """
    Test if the generate_attack function returns a tuple.
    """
    try:
        mp_game_engine = importlib.import_module('battleships.mp_game_engine')
        assert isinstance(mp_game_engine.generate_attack(), tuple)
    except AssertionError:
        testReport.add_message("generate_attack function does not return a tuple")
        pytest.fail("generate_attack function does not return a tuple")


@pytest.mark.depends(on=["test_mp_game_engine_exists"])
def test_generate_attack_in_range():
    """
    Test if the generate_attack function returns a tuple.
    """
    try:
        mp_game_engine = importlib.import_module('battleships.mp_game_engine')
        components = importlib.import_module('battleships.components')
        # Since this function is a random coordinate we'll run it many times to check
        # its always in range, also test it for multiple sizes
        for i in range(200):
            size = 10
            test_board = components.initialise_board(size)
            coordinate = mp_game_engine.generate_attack(test_board)
            assert 0 <= coordinate[0] < size and 0 <= coordinate[1] < size

            size = 20
            test_board = components.initialise_board(size)
            coordinate = mp_game_engine.generate_attack(test_board)
            assert 0 <= coordinate[0] < size and 0 <= coordinate[1] < size

            size = 5
            test_board = components.initialise_board(size)
            coordinate = mp_game_engine.generate_attack(test_board)
            assert 0 <= coordinate[0] < size and 0 <= coordinate[1] < size
    except AssertionError:
        testReport.add_message("generate_attack function does not return a tuple")
        pytest.fail("test_generate_attack_return_type failed")
