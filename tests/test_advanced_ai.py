"""
This module runs unit tests for advanced_ai.py file
Authors:
Student 130003140 (Test Functions)
"""

import importlib
# import inspect
# from copy import deepcopy
import pytest
import test_helper_functions as thf

testReport = thf.TestReport("test_report.txt")


@pytest.mark.dependency()
def test_advanced_ai_exists() -> None:
    """
    Test if the advanced_ai module exists.
    :return: None
    """

    try:
        importlib.import_module('battleships.advanced_ai')
    except ImportError:
        testReport.add_message("advanced_ai module does not exist in your solution.")
        pytest.fail("advanced_ai module does not exist")


##########################################################################
# Test attack methods
##########################################################################
@pytest.mark.dependency(depends=["test_advanced_ai_exists"])
def test_generate_advanced_attack_1unsunk() -> None:
    """
    Test if the generate_advanced_attack function works error free when it knows
    The position of 1 unsunk ship
    :return: None
    """

    try:
        ai = importlib.import_module('battleships.advanced_ai')
        # This scenario is for when we have one unsunk hit so we can't form a line with it yet
        org_board = [[None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None],
                     [None, None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None, None],
                     [None, None, 'Aircraft_Carrier', 'Aircraft_Carrier', 'Aircraft_Carrier',
                      'Aircraft_Carrier', 'Aircraft_Carrier', None, None, None],
                     [None, None, None, None, 'Battleship', 'Battleship', 'Battleship',
                      'Battleship', None, None],
                     [None, None, None, None, None, None, None, None, None, None],
                     [None, 'Submarine', None, None, None, None, 'Destroyer', None, None, None],
                     [None, 'Submarine', None, None, None, None, 'Destroyer', None, None, None],
                     [None, 'Submarine', None, None, None, None, None, None, None, None]]

        board = [[None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, 'Submarine', None, None, None, None, None, None, None, None],
                 [None, 'Submarine', None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None]]
        enemy_dict = {'board': board,
                      'ships': {'Aircraft_Carrier': 0, 'Battleship': 0, 'Cruiser': 0,
                                'Submarine': 2, 'Destroyer': 0},
                      'original_board': org_board}

        our_history = [(5, 5), (5, 4), (5, 6), (5, 3), (4, 5), (6, 5), (7, 5), (4, 4),
                       (3, 4), (2, 4), (6, 4), (2, 7), (7, 2), (1, 2), (6, 7), (6, 8),
                       (3, 1), (6, 1), (3, 8), (1, 5), (8, 6), (4, 2), (8, 3), (2, 3),
                       (7, 9), (9, 4), (2, 0), (0, 6), (4, 9), (9, 7), (5, 0), (6, 0),
                       (7, 0), (4, 0), (9, 1), (0, 1), (3, 6), (1, 9)]

        # Test with all different modes to check it doesn't fail
        # Given theres a random element to all attack modes, run these many times to check
        for _ in range(20):
            assert ai.generate_advanced_attack(0, enemy_dict, our_history)
            assert ai.generate_advanced_attack(1, enemy_dict, our_history)
            assert ai.generate_advanced_attack(2, enemy_dict, our_history)
            assert ai.generate_advanced_attack(3, enemy_dict, our_history)
            assert ai.generate_advanced_attack(4, enemy_dict, our_history)

    except AssertionError:
        testReport.add_message('test_generate_advanced_attack_1unsunk failed')
        pytest.fail('test_generate_advanced_attack_1unsunk failed')


@pytest.mark.dependency(depends=["test_advanced_ai_exists"])
def test_generate_advanced_attack_blind_intelligent() -> None:
    """
    Test if the generate_advanced_attack function works error free when it knows
    The position of no unsunk ships so it guesses blind
    :return: None
    """

    try:
        ai = importlib.import_module('battleships.advanced_ai')

        # This scenario is for if we have no unsunk hits so we use blind guessing
        board = [[None, None, 'Destroyer', 'Destroyer', None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, 'Submarine'],
                 [None, None, None, None, None, None, None, None, None, 'Submarine'],
                 [None, None, None, None, None, None, None, None, None, 'Submarine'],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser']]
        org_board = [[None, None, 'Destroyer', 'Destroyer', None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None, 'Submarine'],
                     [None, None, None, None, None, None, None, None, None, 'Submarine'],
                     [None, None, 'Aircraft_Carrier', 'Aircraft_Carrier', 'Aircraft_Carrier',
                      'Aircraft_Carrier',
                      'Aircraft_Carrier', None, None, 'Submarine'],
                     [None, None, None, None, None, None, None, None, None, None],
                     [None, None, 'Battleship', None, None, None, None, None, None, None],
                     [None, None, 'Battleship', None, None, None, None, None, None, None],
                     [None, None, 'Battleship', None, None, None, None, None, None, None],
                     [None, None, 'Battleship', None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser']]
        enemy_dict = {'board': board,
                      'ships': {'Aircraft_Carrier': 0, 'Battleship': 0,
                                'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2},
                      'original_board': org_board}
        our_history = [(5, 5), (4, 4), (6, 3), (5, 3), (7, 3),
                       (4, 3), (3, 3), (2, 3), (3, 6), (6, 7),
                       (2, 7), (2, 8), (2, 9), (2, 6), (2, 5)]
        # Test with all different modes to check it doesn't fail
        # Given theres a random element to all attack modes, run these many times to check
        for _ in range(20):
            assert ai.generate_advanced_attack(0, enemy_dict, our_history)
            assert ai.generate_advanced_attack(1, enemy_dict, our_history)
            assert ai.generate_advanced_attack(2, enemy_dict, our_history)
            assert ai.generate_advanced_attack(3, enemy_dict, our_history)
            assert ai.generate_advanced_attack(4, enemy_dict, our_history)

    except AssertionError:
        testReport.add_message('test_generate_advanced_attack_blind_intelligent failed')
        pytest.fail('test_generate_advanced_attack_blind_intelligent failed')


@pytest.mark.dependency(depends=["test_advanced_ai_exists"])
def test_generate_advanced_attack_line_unsunk() -> None:
    """
    Test if the generate_advanced_attack function works error free when it knows
    The position of >1 unsunk ship so it can form a line
    :return: None
    """

    try:
        ai = importlib.import_module('battleships.advanced_ai')
        # This scenario is for testing in a line of unsunk hits

        our_history = [(5, 5), (6, 5), (4, 5), (7, 5), (3, 4),
                       (2, 6), (5, 2), (5, 1), (5, 3), (6, 2),
                       (4, 2), (3, 2), (2, 2), (1, 2), (3, 7),
                       (8, 6), (6, 8), (7, 7), (1, 5), (1, 4), (1, 3)]
        board = [[None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None, None, None],
                 [None, 'Battleship', None, None, None, 'Submarine', None, None, None, None],
                 [None, 'Battleship', None, None, None, 'Submarine', None, None, 'Destroyer', None],
                 [None, None, None, None, None, 'Submarine', None, None, 'Destroyer', None],
                 [None, None, None, None, None, None, None, None, None, None]]
        org_board = [[None, None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None, None],
                     [None, 'Aircraft_Carrier', 'Aircraft_Carrier', 'Aircraft_Carrier',
                      'Aircraft_Carrier', 'Aircraft_Carrier', None, None, None, None],
                     [None, None, None, None, None, None, None, None, None, None],
                     [None, 'Battleship', None, None, None, None, None, None, None, None],
                     [None, 'Battleship', None, None, None, 'Cruiser', 'Cruiser', 'Cruiser', None,
                      None],
                     [None, 'Battleship', None, None, None, 'Submarine', None, None, None, None],
                     [None, 'Battleship', None, None, None, 'Submarine', None, None, 'Destroyer',
                      None],
                     [None, None, None, None, None, 'Submarine', None, None, 'Destroyer', None],
                     [None, None, None, None, None, None, None, None, None, None]]
        enemy_dict = {'board': board,
                      'ships': {'Aircraft_Carrier': 0, 'Battleship': 2,
                                'Cruiser': 0, 'Submarine': 3, 'Destroyer': 2},
                      'original_board': org_board}

        for _ in range(20):
            assert ai.generate_advanced_attack(0, enemy_dict, our_history)
            assert ai.generate_advanced_attack(1, enemy_dict, our_history)
            assert ai.generate_advanced_attack(2, enemy_dict, our_history)
            assert ai.generate_advanced_attack(3, enemy_dict, our_history)
            assert ai.generate_advanced_attack(4, enemy_dict, our_history)

    except AssertionError:
        testReport.add_message('test_generate_advanced_attack_line_unsunk failed')
        pytest.fail('test_generate_advanced_attack_line_unsunk failed')


@pytest.mark.dependency(depends=["test_advanced_ai_exists"])
def test_generate_advanced_attack_args_invalid() -> None:
    """
    Test giving invalid arguments to the function
    :return: None
    """
    try:
        ai = importlib.import_module('battleships.advanced_ai')

        difficulty = 2
        enemy_dict = {'board': [[None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None]],
                      'ships': {'Aircraft_Carrier': 0, 'Battleship': 2,
                                'Cruiser': 0, 'Submarine': 3, 'Destroyer': 2},
                      'original_board': [[None, None, None, None, None],
                                         [None, None, None, None, None],
                                         [None, None, None, None, None],
                                         [None, None, None, None, None],
                                         [None, None, None, None, None]]}
        our_history = [(0, 0), (1, 2), (3, 4), (1, 2), (1, 4)]

        # Test non int difficulty
        with pytest.raises(TypeError):
            ai.generate_advanced_attack('one', enemy_dict, our_history)
        # Test non dict enemy_dict
        with pytest.raises(TypeError):
            ai.generate_advanced_attack(difficulty, 'enemy_dict', our_history)
        # Test non list history
        with pytest.raises(TypeError):
            ai.generate_advanced_attack(difficulty, enemy_dict, 'our_history')

        # Test out of range difficulty
        with pytest.raises(ValueError):
            ai.generate_advanced_attack(-1, enemy_dict, our_history)
        # Test out of range difficulty
        with pytest.raises(ValueError):
            ai.generate_advanced_attack(5, enemy_dict, our_history)

    except AssertionError as msg:
        testReport.add_message('test_generate_advanced_attack_args_invalid failed')
        pytest.fail(msg)


##########################################################################
# Test incomplete data dictionaries
# Common test in most functions in advanced_ai module
##########################################################################
@pytest.mark.dependency(depends=["test_advanced_ai_exists"])
def test_incomplete_dicts() -> None:
    """
    Test incomplete data dictionaries
    Common test in most functions in advanced_ai module
    :return: None
    """
    try:
        ai = importlib.import_module('battleships.advanced_ai')

        enemy_dict_incomplete_1 = {
            'ships': {'Aircraft_Carrier': 0, 'Battleship': 2,
                      'Cruiser': 0, 'Submarine': 3, 'Destroyer': 2},
            'original_board': [[None, None, None, None, None],
                               [None, None, None, None, None],
                               [None, None, None, None, None],
                               [None, None, None, None, None],
                               [None, None, None, None, None]]}

        enemy_dict_incomplete_2 = {'board': [[None, None, None, None, None],
                                             [None, None, None, None, None],
                                             [None, None, None, None, None],
                                             [None, None, None, None, None],
                                             [None, None, None, None, None]],
                                   }
        our_history = [(0, 0), (1, 2), (3, 4), (1, 2), (1, 4)]

        # Test with one incomplete dictionaries in generate_advanced_attack
        with pytest.raises(ValueError):
            ai.generate_advanced_attack(1, enemy_dict_incomplete_1, our_history)

        # Test with two incomplete dictionaries in generate_attack_difficulty_2
        with pytest.raises(ValueError):
            ai.generate_attack_difficulty_2(enemy_dict_incomplete_1, our_history)
        with pytest.raises(ValueError):
            ai.generate_attack_difficulty_2(enemy_dict_incomplete_2, our_history)

        # Test with two incomplete dictionaries in generate_attack_difficulty_3
        with pytest.raises(ValueError):
            ai.generate_attack_difficulty_3(enemy_dict_incomplete_1, our_history)
        with pytest.raises(ValueError):
            ai.generate_attack_difficulty_3(enemy_dict_incomplete_2, our_history)

        # Test with two incomplete dictionaries in generate_attack_difficulty_4
        with pytest.raises(ValueError):
            ai.generate_attack_difficulty_4(enemy_dict_incomplete_1, our_history)
        with pytest.raises(ValueError):
            ai.generate_attack_difficulty_4(enemy_dict_incomplete_2, our_history)

        # Test with two incomplete dictionaries in generate_intelligent_blind_guess
        with pytest.raises(ValueError):
            ai.generate_intelligent_blind_guess(enemy_dict_incomplete_1, our_history)
        with pytest.raises(ValueError):
            ai.generate_intelligent_blind_guess(enemy_dict_incomplete_2, our_history)

        # Test with two incomplete dictionaries in guess_line_attack
        with pytest.raises(ValueError):
            ai.guess_line_attack(enemy_dict_incomplete_1, our_history)
        with pytest.raises(ValueError):
            ai.guess_line_attack(enemy_dict_incomplete_2, our_history)

    except AssertionError as msg:
        testReport.add_message('test_incomplete_dicts failed')
        pytest.fail(msg)
