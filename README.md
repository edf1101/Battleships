# ECM1400 Battleships

## Introduction
A python application to simulate a Battleships game against an AI in both a command line interface and a Flask GUI.

## Coursework Self assessment
All features required by specification are complete.
### Additional 
#### Entry Screen
The user can select the game settings (size, difficulty, storms) on an Entry page.
Game screen has a return to menu button
#### Storm Mode
When this is turned on The board will shift 1 space each turn in a predetermined direction
#### [Guess Boards](gui_extensions.py)
For the main script I changed the mechanics. Each user has a board and a guess board. The guess board holds a copy of the enemy's 
original board. As a user guesses their guess board updates showing each hit, miss or sink.
this means we can have a guess history, making the AI more intelligent.
#### HTML Template modifications
You now send the user's guess board and board to the Flask interface, and it renders that, the HTML does no processing
of AI's guesses anymore, also can display if ships are sunk
#### AI attacking
There are 5 AI difficulties [code here](advanced_attacking.py)
- Pure Random Guessing
- Random but it won't guess same space twice
- Intelligent Guessing where it uses previous guesses to guess around hits (or trying to follow lines of hits) There are 3 semi-levels of difficulty for this mode

Wrote [a script](ai_comparison.py) to test AI's against each other
![alt text](static/images/AI%20scoring%20image.png)

## Prerequisites
- Flask must be installed
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


## Details
#### License
MIT License: [found here](LICENSE)

#### Authors
- Ed Fillingham
- Matt Collison (Flask template, unit tests)

#### Source
Code can be found online at https://github.com/edf1101/Battleships/