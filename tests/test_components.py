"""
This module runs unit tests for components.py file
Authors:
Ed Fillingham (Additional Test Functions)
Matt Collison (Example Unit Tests provided)
"""

import importlib
import inspect
from copy import deepcopy
import pytest
import test_helper_functions as thf

testReport = thf.TestReport("../test_report.txt")


@pytest.mark.dependency()
def test_components_exists() -> None:
    """
    Test if the components module exists.
    :return: None
    """

    try:
        importlib.import_module('components')
    except ImportError:
        testReport.add_message("components module does not exist in your solution.")
        pytest.fail("components module does not exist")


##########################################################################
# Test initialise_board function
##########################################################################
@pytest.mark.dependency(depends=["test_components_exists"])
def test_initialise_board_return_size() -> None:
    """
    Test if the initialise_board function returns a list of the correct size.
    :return: None
    """

    components = importlib.import_module('components')

    size = 10
    # Run the function
    board = components.initialise_board(size)
    # Check that the return is a list
    assert isinstance(board, list), "initialise_board function does not return a list"
    # check that the length of the list is the same as board
    assert len(board) == size, ("initialise_board function does not return a"
                                " list of the correct size")
    for row in board:
        # Check that each sub element is a list
        assert isinstance(row, list), "initialise_board function does not return a list of lists"
        # Check that each sub list is the same size as board
        assert len(row) == size, ("initialise_board function does not return lists"
                                  " of the correct size")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_initialise_board_return_none() -> None:
    """
    Test that all the values in the list of list returned by initialise_board are None
    :return: None
    """
    components = importlib.import_module('components')
    size = 10
    # Run the function
    board = components.initialise_board(size)

    for row in board:
        for cell in row:
            assert cell is None, ("initialise_board function does not return a list of lists "
                                  "that are ALL None")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_initialise_board_invalid_arguments() -> None:
    """
    Tests that if you enter invalid parameters for initialise board it throws an error
    Testing if size = string or if size is smaller than 1
    :return: None
    """
    components = importlib.import_module('components')
    with pytest.raises(TypeError):
        components.initialise_board('ten')

    with pytest.raises(ValueError):
        components.initialise_board(-1)


@pytest.mark.dependency(depends=["test_components_exists"])
def test_initialise_board_argument():
    """
    Test if the initialise_board function accepts an integer argument.
    """
    components = importlib.import_module('components')

    try:
        components.initialise_board(10)
    except TypeError:
        testReport.add_message("initialise_board function does not accept an integer argument")
        pytest.fail("initialise_board function does not accept an integer argument")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_initialise_board_return_type():
    """
    Test if the initialise_board function returns a list.
    """
    components = importlib.import_module('components')

    try:
        assert thf.is_list_of_lists(components.initialise_board(10), str)
    except AssertionError:
        testReport.add_message("initialise_board function does not return a list")
        pytest.fail("initialise_board function does not return a list")


##########################################################################
# Test create_battleships function
##########################################################################
@pytest.mark.dependency(depends=["test_components_exists"])
def test_create_battleships_exists():
    """
    Test if the create_battleships function exists.
    """
    components = importlib.import_module('components')

    try:
        assert hasattr(components, 'create_battleships'), ("create_battleships function "
                                                           "does not exist")
    except AssertionError:
        testReport.add_message("create_battleships function does not exist in your solution.")
        pytest.fail("create_battleships function does not exist")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_battleships_txt_exists():
    """
    Test if the battleships.txt file exists.
    """

    try:
        with open("../battleships.txt", 'r', encoding="utf-8"):
            pass
    except FileNotFoundError:
        testReport.add_message("battleships.txt file does not exist in your solution.")
        pytest.fail("battleships.txt file does not exist")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_create_battleships_argument():
    """
    Test if the create_battleships function accepts a string argument.
    """
    components = importlib.import_module('components')

    try:
        components.create_battleships("battleships.txt")
    except TypeError:
        testReport.add_message("create_battleships function does not accept a string argument")
        pytest.fail("create_battleships function does not accept a string argument")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_create_battleships_return_type():
    """
    Test if the create_battleships function returns a dictionary.
    """
    components = importlib.import_module('components')

    try:
        assert thf.is_dict_of_type(components.create_battleships("battleships.txt"), str, int)
    except AssertionError:
        testReport.add_message("create_battleships function does not return a dictionary")
        pytest.fail("create_battleships function does not return a dictionary")


##########################################################################
# Test place_battleships function
##########################################################################
@pytest.mark.dependency(depends=["test_components_exists"])
def test_place_battleships_exists():
    """
    Test if the place_battleships function exists.
    """
    components = importlib.import_module('components')

    try:
        assert hasattr(components, 'place_battleships'), "place_battleships function does not exist"
    except AssertionError:
        testReport.add_message("place_battleships function does not exist in your solution.")
        pytest.fail("place_battleships function does not exist")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_place_battleships_arguments():
    """
    Test if the place_battleships function accepts a list and a dictionary argument.
    """
    components = importlib.import_module('components')

    try:
        # Check to make sure the place_battleships function has a board ships and algorithm argument
        assert "board" in inspect.signature(components.place_battleships).parameters, \
            ("place_battleships function"
             "does not have a board argument")
        assert "ships" in inspect.signature(components.place_battleships).parameters, \
            ("place_battleships function "
             "does not have a ships argument")
        assert "algorithm" in inspect.signature(components.place_battleships).parameters, \
            ("place_battleships function "
             "does not have a algorithm "
             "argument")
    except AssertionError:
        testReport.add_message("place_battleships function is missing an argument."
                               "Check your function has a board, ships and algorithm argument")
        pytest.fail("place_battleships function does not have a board, ships and algorithm"
                    " argument")

    try:
        board = components.initialise_board(10)
        ships = components.create_battleships("battleships.txt")
        components.place_battleships(board, ships)
    except TypeError:
        testReport.add_message("place_battleships function does not accept a list"
                               " and a dictionary argument")
        pytest.fail("place_battleships function does not accept a list and a "
                    "dictionary argument")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_place_battleships_return_type():
    """
    Test if the place_battleships function returns a list of lists of strings/None values.
    """
    components = importlib.import_module('components')

    board = components.initialise_board(10)
    ships = components.create_battleships("battleships.txt")
    try:
        assert thf.is_list_of_lists(components.place_battleships(board, ships), str), \
            ("place_battleships function "
             "does not return a list of "
             "lists of strings/None values")
    except AssertionError:
        testReport.add_message("place_battleships function does not return a list of"
                               " lists of strings/None values")
        pytest.fail("place_battleships function does not return a list of lists of "
                    "list of strings/None")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_place_battleships_argument_errors() -> None:
    """
    Test what happens if we give invalid value arguments to the function place_battleships
    :return: None
    """
    components = importlib.import_module('components')
    board = components.initialise_board(10)
    ships = components.create_battleships("battleships.txt")
    with pytest.raises(ValueError):
        components.place_battleships(board, ships, algorithm='nonsense Algorithm')

    # Test giving it a board that's nothing
    board = []
    with pytest.raises(ValueError):
        components.place_battleships(board, ships)

    # Test what happens if we pass a string as the board parameter
    with pytest.raises(TypeError):
        components.place_battleships('board', ships)

    board = components.initialise_board(10)
    # Test giving it a ships parameter that's nothing
    ships = {}
    with pytest.raises(ValueError):
        components.place_battleships(board, ships)

    # Test what happens if we pass a string as the ships parameter
    with pytest.raises(TypeError):
        components.place_battleships(board, 'ships')


@pytest.mark.dependency(depends=["test_components_exists"])
def test_place_battleships_functionality() -> None:
    """
    Test that the function gives expected outputs
    :return: None
    """
    components = importlib.import_module('components')

    # Test if the simple mode works
    board = components.initialise_board(5)
    ships = {'Submarine': 3, 'Destroyer': 2}

    test_board = components.place_battleships(deepcopy(board), ships, algorithm='simple')
    expected_board = [['Submarine', 'Submarine', 'Submarine', None, None],
                      ['Destroyer', 'Destroyer', None, None, None],
                      [None, None, None, None, None],
                      [None, None, None, None, None],
                      [None, None, None, None, None]]

    assert expected_board == test_board, "The simple function doesn't work"

    # For the random mode we will just test that there are the correct number of tiles across
    # the board as ships dict requires
    board = components.initialise_board(5)
    ships = {'Submarine': 3, 'Destroyer': 2}
    test_board = components.place_battleships(deepcopy(board), ships, algorithm='simple')

    for ship, expected_count in ships.items():
        count = 0
        for row in test_board:
            for cell in row:
                if cell == ship:
                    count += 1
        assert count == expected_count, "The random function doesn't work"


##########################################################################
# Test in_board function
##########################################################################
@pytest.mark.dependency(depends=["test_components_exists"])
def test_in_board_arguments():
    """
    Test if the in_board function accepts correct arguments.
    """
    components = importlib.import_module('components')

    try:
        # Check to make sure the place_battleships function has a board ships and algorithm argument
        assert "location" in inspect.signature(components.in_board).parameters, \
            "location not in in_board function"
        assert "board" in inspect.signature(components.in_board).parameters, \
            "board not in in_board function"

    except AssertionError:
        testReport.add_message("in_board function is missing an argument.")
        pytest.fail("in_board function does not have right arguments")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_in_board_functionality():
    """
    Test that the function gives expected outputs
    :return: None
    """
    components = importlib.import_module('components')

    board = components.initialise_board(5)

    # Edge cases
    assert components.in_board((-1, 0), board) is False, "Function failed"
    assert components.in_board((0, 0), board) is True, "Function failed"
    assert components.in_board((5, 5), board) is False, "Function failed"

    # True examples
    assert components.in_board((2, 2), board) is True, "Function failed"


