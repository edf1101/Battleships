# ECM1400 Battleships

## Introduction
A python application to simulate a Battleships game against an AI in both a command line interface and a Flask GUI.

## Coursework Self assessment
All features required by specification are complete.
### Additional 
#### Entry Screen
The user can select the game settings (size, difficulty) on an Entry page.
Game screen has a return to menu button so games can be replayed
#### Storm Mode
When this is turned on The board will shift 1 space each turn in a predetermined direction
#### HTML Template sunken ships
If a ship has been sunk, the main.py script sends a list of sunk positions for
either the AI or Player to the HTML code, and it colours those tiles green
#### AI attacking
There are 5 AI difficulties [code here](advanced_ai.py)
0. Pure Random Guessing
1. Random but it won't guess same space twice
2. Guessing a random position around unsunk hits
3. Trying to guess in a line around unsunk hits
4. Guesses in a line if there are unsunk hits, if none it calculates the probability of a ship being in any 
unguessed tile and guesses there

Wrote [a script](ai_comparison.py) to test AI's against each other

<img src="static/images/AI scoring 2.png" alt="drawing" width="500"/>
<img src="static/images/AI scoring image.png" alt="drawing" width="500"/> 

## Prerequisites
- Flask must be installed ```pip install Flask```
- numpy must be installed ```pip install numpy```
- Python version must be ≥ 3.10 due to ```|``` symbol in typehinting

_Version used in running = Python 3.11.4_

## Installation
Run in Terminal ``` pip install Flask```

## Getting Started
There are 3 modes to run the game:
- Run the [game_engine file](game_engine.py) as a module for a CLI game against yourself
- Run the [mp_game_engine file](mp_game_engine.py) for a CLI game against an AI
- Run the [main file](main.py) for a full GUI game


## Documentation
[Code documentation can be found here](docs/index.html)

## Details
#### License
MIT License: [found here](LICENSE)

#### Authors
- Ed Fillingham

#### Source
Code hosted (privately) at https://github.com/edf1101/Battleships/
