"""
This module runs unit tests for components.py file
Authors:
Student 130003140 (Additional Test Functions)
Matt Collison (Example Unit Tests provided)
"""

import importlib
import inspect
from copy import deepcopy
import pytest
import test_helper_functions as thf

testReport = thf.TestReport("test_report.txt")


@pytest.mark.dependency()
def test_components_exists() -> None:
    """
    Test if the components module exists.
    :return: None
    """

    try:
        importlib.import_module('battleships.components')
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

    try:
        components = importlib.import_module('battleships.components')

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
            assert isinstance(row, list), \
                "initialise_board function does not return a list of lists"
            # Check that each sub list is the same size as board
            assert len(row) == size, ("initialise_board function does not return lists"
                                      " of the correct size")
    except AssertionError as msg:
        testReport.add_message('test_initialise_board_return_size failed')
        pytest.fail(msg)


@pytest.mark.dependency(depends=["test_components_exists"])
def test_initialise_board_return_none() -> None:
    """
    Test that all the values in the list of list returned by initialise_board are None
    :return: None
    """
    try:
        components = importlib.import_module('battleships.components')
        size = 10
        # Run the function
        board = components.initialise_board(size)

        for row in board:
            for cell in row:
                assert cell is None, ("initialise_board function does not return a list of lists "
                                      "that are ALL None")

    except AssertionError as msg:
        testReport.add_message('test_initialise_board_return_none failed')
        pytest.fail(msg)


@pytest.mark.dependency(depends=["test_components_exists"])
def test_initialise_board_invalid_arguments() -> None:
    """
        Tests that if you enter invalid parameters for initialise board it throws an error
        Testing if size = string or if size is smaller than 1
        :return: None
        """
    try:
        components = importlib.import_module('battleships.components')
        with pytest.raises(TypeError):
            components.initialise_board('ten')

        with pytest.raises(ValueError):
            components.initialise_board(-1)

    except AssertionError as msg:
        testReport.add_message('test_initialise_board_invalid_arguments failed')
        pytest.fail(msg)


@pytest.mark.dependency(depends=["test_components_exists"])
def test_initialise_board_argument() -> None:
    """
    Test if the initialise_board function accepts an integer argument.
    """
    try:
        components = importlib.import_module('battleships.components')

        try:
            components.initialise_board(10)
        except TypeError:
            testReport.add_message("initialise_board function does not accept an integer argument")
            pytest.fail("initialise_board function does not accept an integer argument")

    except AssertionError as msg:
        testReport.add_message('test_initialise_board_argument failed')
        pytest.fail(msg)


@pytest.mark.dependency(depends=["test_components_exists"])
def test_initialise_board_return_type() -> None:
    """
    Test if the initialise_board function returns a list.
    """
    try:
        components = importlib.import_module('battleships.components')

        try:
            assert thf.is_list_of_lists(components.initialise_board(10), str)
        except AssertionError:
            testReport.add_message("initialise_board function does not return a list")
            pytest.fail("initialise_board function does not return a list")
    except AssertionError as msg:
        testReport.add_message('test_initialise_board_return_type failed')
        pytest.fail(msg)


##########################################################################
# Test create_battleships function
##########################################################################
@pytest.mark.dependency(depends=["test_components_exists"])
def test_create_battleships_exists() -> None:
    """
    Test if the create_battleships function exists.
    """
    components = importlib.import_module('battleships.components')

    try:
        assert hasattr(components, 'create_battleships'), ("create_battleships function "
                                                           "does not exist")
    except AssertionError:
        testReport.add_message("create_battleships function does not exist in your solution.")
        pytest.fail("create_battleships function does not exist")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_battleships_txt_exists() -> None:
    """
    Test if the battleships.txt file exists.
    """

    try:
        with open("../battleships/battleships.txt", 'r', encoding="utf-8"):
            pass
    except FileNotFoundError:
        testReport.add_message("battleships.txt file does not exist in your solution.")
        pytest.fail("battleships.txt file does not exist")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_create_battleships_argument() -> None:
    """
    Test if the create_battleships function accepts a string argument.
    """
    components = importlib.import_module('battleships.components')

    try:
        components.create_battleships("battleships.txt")
    except TypeError:
        testReport.add_message("create_battleships function does not accept a string argument")
        pytest.fail("create_battleships function does not accept a string argument")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_create_battleships_return_type() -> None:
    """
    Test if the create_battleships function returns a dictionary.
    """
    components = importlib.import_module('battleships.components')

    try:
        assert thf.is_dict_of_type(components.create_battleships("battleships.txt"), str, int)
    except AssertionError:
        testReport.add_message("create_battleships function does not return a dictionary")
        pytest.fail("create_battleships function does not return a dictionary")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_create_battleships_invalid_args() -> None:
    """
    Tests what happens if we give it invalid arguments
    """
    components = importlib.import_module('battleships.components')

    try:

        with pytest.raises(ValueError):
            components.create_battleships('battleships')
        with pytest.raises(TypeError):
            components.create_battleships(123)

        # Test what happens if we give a not formatted well battleships file
        with pytest.raises(ValueError):
            components.create_battleships('invalid_battleships.txt')

    except AssertionError:
        testReport.add_message("test_create_battleships_invalid_args test Failed")
        pytest.fail("test_create_battleships_invalid_args test Failed")


##########################################################################
# Test place_battleships function
##########################################################################
@pytest.mark.dependency(depends=["test_components_exists"])
def test_place_battleships_exists() -> None:
    """
    Test if the place_battleships function exists.
    """
    components = importlib.import_module('battleships.components')

    try:
        assert hasattr(components, 'place_battleships'), "place_battleships function does not exist"
    except AssertionError:
        testReport.add_message("place_battleships function does not exist in your solution.")
        pytest.fail("place_battleships function does not exist")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_place_battleships_arguments() -> None:
    """
    Test if the place_battleships function accepts a list and a dictionary argument.
    """
    components = importlib.import_module('battleships.components')

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
def test_place_battleships_return_type() -> None:
    """
    Test if the place_battleships function returns a list of lists of strings/None values.
    """
    components = importlib.import_module('battleships.components')

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

    try:
        components = importlib.import_module('battleships.components')
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

    except AssertionError as msg:
        testReport.add_message('test_place_battleships_argument_errors failed')
        pytest.fail(msg)


@pytest.mark.dependency(depends=["test_components_exists"])
def test_place_battleships_functionality() -> None:
    """
    Test that the function gives expected outputs
    :return: None
    """

    try:

        components = importlib.import_module('battleships.components')

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
        ships = {'Submarine': 3, 'Destroyer': 2, 'Tester': 4}
        test_board = components.place_battleships(deepcopy(board), ships, algorithm='random')

        for ship, expected_count in ships.items():
            count = 0
            for row in test_board:
                for cell in row:
                    if cell == ship:
                        count += 1
            assert count == expected_count, "The random function doesn't work"

        # Test place battleships custom
        expected_board = [['Submarine', 'Submarine', 'Submarine', None, None],
                          [None, None, None, None, None],
                          [None, None, None, None, None],
                          [None, None, None, None, None],
                          [None, None, None, None, None]]
        test_board = components.place_battleships(deepcopy(board), ships,
                                                  algorithm='custom',
                                                  use_absolute_path=False)
        assert test_board == expected_board, "Custom algorithm doesn't work"

    except AssertionError as msg:
        testReport.add_message('test_place_battleships_functionality failed')
        pytest.fail(msg)


##########################################################################
# Test in_board function
##########################################################################
@pytest.mark.dependency(depends=["test_components_exists"])
def test_in_board_exists() -> None:
    """
    Test if the place_battleships function exists.
    """
    components = importlib.import_module('battleships.components')

    try:
        assert hasattr(components, 'in_board'), "in_board function does not exist"
    except AssertionError:
        testReport.add_message("in_board function does not exist in your solution.")
        pytest.fail("in_board function does not exist")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_in_board_arguments() -> None:
    """
    Test if the in_board function accepts correct arguments.
    """
    components = importlib.import_module('battleships.components')

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
def test_in_board_functionality() -> None:
    """
    Test that the function gives expected outputs
    :return: None
    """
    try:
        components = importlib.import_module('battleships.components')

        board = components.initialise_board(5)

        # Edge cases
        assert components.in_board((-1, 0), board) is False, "Function failed"
        assert components.in_board((0, 0), board) is True, "Function failed"
        assert components.in_board((5, 5), board) is False, "Function failed"

        # True examples
        assert components.in_board((2, 2), board) is True, "Function failed"

    except AssertionError as msg:
        testReport.add_message('test_in_board_functionality failed')
        pytest.fail(msg)


@pytest.mark.dependency(depends=["test_components_exists"])
def test_in_board_invalid_arguments() -> None:
    """
    Test that the function throws correct errors when given wrong arguments
    :return: None
    """
    try:
        components = importlib.import_module('battleships.components')

        board = components.initialise_board(5)

        # Test giving board parameter as a string not a list of lists
        with pytest.raises(TypeError):
            components.in_board((2, 2), 'board')

        # Test giving incorrect parameter for location should be tuple[int,int]
        with pytest.raises(TypeError):
            components.in_board([2, 2], board)

        # Test giving tuple of length 3 for location
        with pytest.raises(ValueError):
            components.in_board((2, 2, 1), board)

        # Test giving a tuple of not int,int
        with pytest.raises(TypeError):
            components.in_board((2, 'a'), board)

    except AssertionError as msg:
        testReport.add_message('test_in_board_invalid_arguments failed')
        pytest.fail(msg)


##########################################################################
# Test try_place_ship function
##########################################################################
@pytest.mark.dependency(depends=["test_components_exists"])
def test_try_place_ship_exists() -> None:
    """
    Test if the place_battleships function exists.
    """
    components = importlib.import_module('battleships.components')

    try:
        assert hasattr(components, 'try_place_ship'), "try_place_ship function does not exist"
    except AssertionError:
        testReport.add_message("try_place_ship function does not exist in your solution.")
        pytest.fail("try_place_ship function does not exist")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_try_place_ship_invalid_arguments() -> None:
    """
    Test that the function throws correct errors when given wrong arguments
    :return: None
    """

    try:
        components = importlib.import_module('battleships.components')

        board = components.initialise_board(5)
        ship_name = 'ship1'
        ship_size = 3
        position = (2, 2)
        orientation = 'h'

        # Test giving board parameter as a string not a list of lists
        with pytest.raises(TypeError):
            components.try_place_ship('board', ship_name, ship_size, position, orientation)

        # Test when we give it a list, but one item in the list isn't a list
        with pytest.raises(TypeError):
            components.try_place_ship([[None, None, None], 'bad'], ship_name,
                                      ship_size, position, 'v')

        # Test giving ship_name parameter as an int not string
        with pytest.raises(TypeError):
            components.try_place_ship(board, 3, ship_size, position, orientation)

        # Test giving ship_size parameter as a string not an int
        with pytest.raises(TypeError):
            components.try_place_ship(board, ship_name, 'three', position, 'h')

        # Test giving position as a non tuple[int,int]
        with pytest.raises(TypeError):
            components.try_place_ship(board, ship_name, ship_size, [2, 3], orientation)
        with pytest.raises(TypeError):
            components.try_place_ship(board, ship_name, ship_size, (1, 'a'), orientation)

        # Test giving orientation as incorrect argument, should be a str of either 'v' or 'h
        with pytest.raises(ValueError):
            components.try_place_ship(board, ship_name, ship_size, position, 't')
        with pytest.raises(TypeError):
            components.try_place_ship(board, ship_name, ship_size, position, 3)

    except AssertionError as msg:
        testReport.add_message('test_try_place_ship_invalid_arguments failed')
        pytest.fail(msg)


@pytest.mark.dependency(depends=["test_components_exists"])
def test_try_place_ship_incorrect_placement() -> None:
    """
    Test that the function gives None back if the parameters for placing a ship are invalid
    :return: None
    """
    try:
        components = importlib.import_module('battleships.components')

        blank_board = components.initialise_board(5)
        ship_name = 'ship1'
        ship_size = 3
        position = (3, 3)
        orientation = 'h'

        assert components.try_place_ship(blank_board, ship_name,
                                         ship_size, position, orientation) is None

        # Try placing a ship on top of another ship by placing a correct ship,
        # then again in the same place
        new_board = components.try_place_ship(blank_board, ship_name,
                                              ship_size, (0, 0), 'v')
        assert components.try_place_ship(new_board, ship_name,
                                         ship_size, (0, 0), 'h') is None

    except AssertionError as msg:
        testReport.add_message('test_try_place_ship_incorrect_placement failed')
        pytest.fail(msg)


@pytest.mark.dependency(depends=["test_components_exists"])
def test_try_place_ship_correct_placement() -> None:
    """
    Test that the function gives the correct board back if the parameters
     for placing a ship are valid
    :return: None
    """

    try:
        components = importlib.import_module('battleships.components')

        blank_board = components.initialise_board(5)
        ship_name = 'ship1'
        ship_size = 3
        position = (2, 2)
        orientation = 'h'

        correct_board = [[None, None, None, None, None],
                         [None, None, None, None, None],
                         [None, None, 'ship1', 'ship1', 'ship1'],
                         [None, None, None, None, None],
                         [None, None, None, None, None]]

        assert components.try_place_ship(blank_board, ship_name,
                                         ship_size, position, orientation) == correct_board

    except AssertionError as msg:
        testReport.add_message('test_try_place_ship_correct_placement failed')
        pytest.fail(msg)


##########################################################################
# Test get_positions_by_name function
##########################################################################
@pytest.mark.depends(on=["test_components_exists"])
def test_get_positions_by_name_exists():
    """
    Test if the get_positions_by_name function exists.
    """
    try:
        components = importlib.import_module('battleships.components')
        assert hasattr(components, 'get_positions_by_name'), \
            "get_positions_by_name function does not exist"
    except AssertionError:
        testReport.add_message("get_positions_by_name function does not exist in your solution.")
        pytest.fail("get_positions_by_name function does not exist")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_get_positions_by_name_arguments() -> None:
    """
    Test if the get_positions_by_name function accepts correct arguments.
    """
    components = importlib.import_module('battleships.components')

    try:
        # Check to make sure the place_battleships function has a board ships and algorithm argument
        assert "names" in inspect.signature(components.get_positions_by_name).parameters, \
            "location not in get_positions_by_name function"
        assert "board" in inspect.signature(components.get_positions_by_name).parameters, \
            "board not in get_positions_by_name function"

    except AssertionError:
        testReport.add_message("get_positions_by_name function is missing an argument.")
        pytest.fail("get_positions_by_name function does not have right arguments")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_get_positions_by_name_invalid_arguments() -> None:
    """
    Test that the function throws correct errors when given wrong arguments
    :return: None
    """

    try:
        components = importlib.import_module('battleships.components')

        # Test giving board parameter as a string not a list of lists
        with pytest.raises(TypeError):
            components.get_positions_by_name('board', ['name1', 'name2'])

        # Test giving board parameter as a list not a list of lists
        with pytest.raises(TypeError):
            components.get_positions_by_name(['board'], ['name1', 'name2'])

        # Test giving names parameter as a non list
        with pytest.raises(TypeError):
            components.get_positions_by_name([[None]], 'single_non_list_name')

    except AssertionError as msg:
        testReport.add_message('test_get_positions_by_name_invalid_arguments failed')
        pytest.fail(msg)


@pytest.mark.dependency(depends=["test_components_exists"])
def test_get_positions_by_name_functionality() -> None:
    """
    Test the get_positions_by_name function works
    """
    try:
        components = importlib.import_module('battleships.components')

        board = [[None, None, 'ship1', 'ship1'],
                 [None, None, None, None],
                 ['ship2', None, None, None]]
        names = ['ship1', 'ship2']

        expected_output = [(2, 0), (3, 0), (0, 2)]
        assert components.get_positions_by_name(board, names) == expected_output, \
            "Didn't find the ships"

    except AssertionError as msg:
        testReport.add_message('test_get_positions_by_name_functionality failed')
        pytest.fail(msg)


##########################################################################
# Test get_sunken_ships function
##########################################################################
@pytest.mark.depends(on=["test_components_exists"])
def test_get_sunken_ships_exists():
    """
    Test if the get_sunken_ships function exists.
    """
    try:
        components = importlib.import_module('battleships.components')
        assert hasattr(components, 'get_sunken_ships'), "get_sunken_ships function does not exist"
    except AssertionError:
        testReport.add_message("get_sunken_ships function does not exist in your solution.")
        pytest.fail("get_sunken_ships function does not exist")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_get_sunken_ships_arguments() -> None:
    """
    Test if the get_sunken_ships function accepts correct arguments.
    """
    components = importlib.import_module('battleships.components')

    try:
        # Check to make sure the place_battleships function has a board ships and algorithm argument
        assert "player_data" in inspect.signature(components.get_sunken_ships).parameters, \
            "location not in get_sunken_ships function"

    except AssertionError:
        testReport.add_message("get_sunken_ships function is missing an argument.")
        pytest.fail("get_sunken_ships function does not have right arguments")


@pytest.mark.dependency(depends=["test_components_exists"])
def test_get_sunken_ships_invalid_arguments() -> None:
    """
    Test that the function throws correct errors when given wrong arguments
    :return: None
    """

    try:
        components = importlib.import_module('battleships.components')

        # Test giving player_data parameter not a complete required dictionary
        # This func need a dict with the keys 'ships' and 'original_board'

        # Test with an empty Dict
        with pytest.raises(ValueError):
            components.get_sunken_ships({})

        # Test with a non dictionary
        with pytest.raises(ValueError):
            components.get_sunken_ships('bad')

        # Test with a dict missing ships
        with pytest.raises(ValueError):
            components.get_sunken_ships({'original_bord': [[None, None]]})

        # Test with a dict missing original_board
        with pytest.raises(ValueError):
            components.get_sunken_ships({'ships': {'ship1': 2}})

    except AssertionError as msg:
        testReport.add_message('test_get_sunken_ships_invalid_arguments failed')
        pytest.fail(msg)


@pytest.mark.dependency(depends=["test_components_exists"])
def test_get_sunken_ships_functionality() -> None:
    """
    Test the get_sunken_ships function works
    """
    try:
        components = importlib.import_module('battleships.components')

        board = [[None, None, 'ship1', 'ship1'],
                 [None, None, None, None],
                 ['ship2', None, None, None]]
        ships = {'ship1': 3, 'ship2': 0}

        player_dict = {"ships": ships, 'original_board': board}

        expected_output = [(0, 2)]  # Expect it to only have found the bottom left sunk ship
        # As the top right is still intact according to ships dict

        assert components.get_sunken_ships(player_dict) == expected_output, "Didn't find the ships"

    except AssertionError as msg:
        testReport.add_message('test_get_positions_by_name_functionality failed')
        pytest.fail(msg)
