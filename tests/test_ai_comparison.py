"""
This module runs unit tests for ai_comparison.py file
Authors:
Student 130003140  (Additional Functionality Tests)
"""

import importlib
import pytest
import test_helper_functions as thf

testReport = thf.TestReport("test_report.txt")


@pytest.mark.depends()
def test_ai_comparison_exists() -> None:
    """
    Test if the game_engine module exists.
    """
    try:
        importlib.import_module('battleships.ai_comparison')
    except ImportError:
        testReport.add_message("ai_comparison module does not exist in your solution.")
        pytest.fail("ai_comparison module does not exist")


############
# Test ai_loop Function
############
@pytest.mark.depends(on=["test_ai_comparison_exists"])
def test_ai_loop_exists() -> None:
    """
    Test if the ai_loop function exists.
    """
    try:
        ai = importlib.import_module('battleships.ai_comparison')
        assert hasattr(ai, 'ai_loop'), "attack function does not exist"
    except AssertionError:
        testReport.add_message("ai_loop function does not exist in your solution.")
        pytest.fail("ai_loop function does not exist")


@pytest.mark.depends(on=["test_ai_comparison_exists"])
def test_ai_loop_arguments() -> None:
    """
    Test if the ai_loop function accepts a tuple, a list, and a dictionary argument.
    """
    try:
        ai = importlib.import_module('battleships.ai_comparison')
        coordinates = (1, 1)
        ai_mode1 = 0
        ai_mode2 = 0
        ai.ai_loop(ai_mode1, ai_mode2)
    except TypeError:
        testReport.add_message("Function doesn't accept the correct arguments")
        pytest.fail("Function doesn't accept the correct arguments")


@pytest.mark.depends(on=["test_ai_comparison_exists"])
def test_ai_loop_arguments_invalid() -> None:
    try:
        ai = importlib.import_module('battleships.ai_comparison')

        # Test non ints for parameters
        with pytest.raises(TypeError):
            ai.ai_loop(1, 'a')

        with pytest.raises(TypeError):
            ai.ai_loop('1', 4)

    except AssertionError as msg:
        testReport.add_message('test_ai_loop_arguments_invalid failed')
        pytest.fail(msg)


@pytest.mark.depends(on=["test_ai_comparison_exists"])
def test_ai_loop_functionality() -> None:
    try:
        # To test it works properly we will test the same AI level against itself
        # the scores should be roughly equal
        ai = importlib.import_module('battleships.ai_comparison')

        # Keeps track of how many times a1 or a2 win
        ai1_score = 0
        ai2_score = 0

        # Run it 2000 number of times
        for i in range(1, 2000):
            winner, moves = ai.ai_loop(0, 0)
            if winner == 'AI1':
                ai1_score += 1
            else:
                ai2_score += 1

        # get the percentage difference in wins
        score_diff_percentage = abs(ai2_score-ai1_score)/20
        # accept a difference of <5%
        assert score_diff_percentage<10
    except AssertionError as msg:
        testReport.add_message('test_ai_loop_functionality failed')
        pytest.fail(msg)
