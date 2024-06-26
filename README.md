# ECM1400 Battleships
<img src="Images/banner.png" alt="drawing" width="800"/>



## Introduction
A python package (availible on PyPi) to simulate a Battleships game against an AI in both a command line interface and a Flask GUI.

## Coursework Self assessment
All features required by specification are complete (including testing & logging). Note: main.py uses classes to avoid global
variables.
### Extensions 
#### Entry Screen
Users can select game settings (size, difficulty, storm mode) on an Entry page.
main.html now has a menu button so games can be replayed.
#### HTML Template Sunken ships
Sunken ship positions for either the AI or Player to the HTML code, and it colours those tiles green.
#### Storm mode
When activated, the player's board shifts one space each turn (as suggested by specification). Since the main.html's grid
isn't persistent this had to be in javascript
#### Packaging
- Packaged with PyPi
- Detailed documentation from sphinx
#### AI attacking
There are 5 difficulties [code here](battleships/advanced_ai.py)

0. Pure Random Guessing
1. Random but it won't guess same space twice
2. Guessing a random position around hits where the ship is still unsunk. If no unsunk hits it guesses randomly
3. Guesses in a line following unsunk hits (more accurate method)
4. Guesses in a line if there are unsunk hits, if not it calculates all possible ship placements in the board
given what's already guessed. Then chooses the tile that has the highest probability of a ship

Wrote [a script](battleships/ai_comparison.py) to score AIs against themselves.

<img src="Images/AI scoring 2.png" alt="drawing" width="500"/>
<img src="Images/AI scoring image.png" alt="drawing" width="500"/> 

## Prerequisites
- Flask must be installed ```pip install Flask```
- numpy must be installed ```pip install numpy```
- For testing pytest must be installed ```pip install pytest``` 
- Pytest plugins must be installed```pip install pytest-depends``` ```pip install pytest-cov```
- Python version must be ≥ 3.10 (pip package requires ≥ 3.11) due to ```|``` symbol in typehinting

_Version used in running = Python 3.11.4_

## Installation and Getting Started
There are 3 modes to run the game:
- Run the [game_engine file](battleships/game_engine.py) as a module for a CLI game against yourself
- Run the [mp_game_engine file](battleships/mp_game_engine.py) for a CLI game against an AI
- Run the [main file](battleships/main.py) for a full GUI game. Once you have run this program navigate to http://127.0.0.1:5000 on a 
browser of choice.

If you are using the Flask (main.py) application then on my version you do not need to enter via /placement. The script 
will automatically render the correct webpage and handle logic (entry, placement or main) depending on your game status.

<br>
There are two ways to install the package:

### pip (recommended)
- In a new venv or for the whole computer run ```pip install battleships-edf1101```
- This will automatically install Flask and numpy
- You can then run ```python -m battleships.main``` or ```python -m battleships.game_engine``` or 
```python -m battleships.mp_game_engine``` to run each mode

### Manually
- Get this repository's folder (clone from github, or download otherwise)
- Open it either either with a virtual environment (useful if using PyCharm) and install Flask and numpy manually as 
shown in prerequisites
- Or you can install Flask and numpy for the whole PC
- To open files you can cd to the battleships directory (the source code folder not the project root) and run ```python -m
main``` (note if you are running it from within the source code directory you don't need to have battleships. prefix)
- Alternatively you could open them manually in a file browser and run them



## Developer Documentation
All documentation for source code [can be found here](docs/_build/html/index.html)

In general
- [Components.py](battleships/components.py): Contains the basic functions for creating Battleships games
- [game_engine.py](battleships/game_engine.py): Contains functions to run a single player game and to run a single player game
- [mp_game_engine.py](battleships/mp_game_engine.py): Contains functions needed for multiplayer games (against AI)
- [main.py](battleships/main.py): Contains the framework needed for a Flask GUI game
- [advanced_ai.py](battleships/advanced_ai.py): Contains the functions needed for the extension 5 versions of AI
- [ai_comparison.py](battleships/ai_comparison.py): Contains functions to compare different versions of AI difficulties

### Testing
If pytest & plugins are installed then you can test in 2 ways.

_Note scripts like game_engine.py, mp_game_engine and main.py don't have full coverage as some functions require input statements which
my unittests were not intended to mock_
1. Use an IDE like PyCharm to run the tests manually
2. Navigate to the tests folder in the project (from the root directory it would be
```cd tests``` then run ```pytest``` )
### pylint
pylint can be run by going to either the root of the project or the source code folder in the terminal then running
```pylint battleships```

### Logging
Logs are taken for error events and for general game actions.

Logs can be found at the working directory for python, this will be different depending on how you installed the package.

## Details
#### License
MIT License: [found here](LICENSE)

#### Authors
- Student 730003140

#### Acknowledgments
This coursework is for the University of Exeter.

Thank you to the Computer Science department.

#### Source
Code hosted (may be public or private depending on time of reading) on [GitHub](https://github.com/edf1101/Battleships/)
Packaged at : [PyPi](https://pypi.org/project/battleships-edf1101/)
