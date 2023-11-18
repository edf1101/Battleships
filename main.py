"""
This is my main code for running a flask battleships game
Includes added extensions:
- Guessboards (holds move histories and can show ships sunk)
- all board processing is done in python and HTML is just sent a copy of
    guessboards  (Means HTML website is persistent)
- Has the storm mode
- Has an entry screen
- Has difficulty modes
"""

# Import flask libs
import random
import json
from flask import Flask
from flask import request
from flask import render_template

# Import gameplay libs
import game_engine
import mp_game_engine
import components
import gui_extensions as gui_ext
import storm_engine

app = Flask(__name__)


@app.route('/placement', methods=['GET', 'POST'])
def placement_interface() -> str:
    """
    This handles the placement menu, so when you first put your ships on the board
    :return: Returns a JSON file if it's a POST request, or the HTML webpage if it's not
    """
    if request.method == 'POST':  # received the JSON data of a board set up
        json_data = request.get_json()

        # so it can redirect to the main game page and start game (outer scope so use global)
        global SET_BOARD
        SET_BOARD = True

        # Because we can only read a JSON ship data from file we need to save it then load it in
        with open("placement.json", "w", encoding="utf-8") as outfile:
            json.dump(json_data, outfile)
        players['Human']['board'] = components.place_battleships(players['Human']['board'],
                                                                 players['Human']['ships'],
                                                                 placement_method='custom')
        # Start the AI's Guess board
        players['AI']['guess_board'] = gui_ext.create_guess_board(players['Human']['board'])

        return json_data  # It wants the data returned to it, so it can check transmission success

    # If it's not a POST request (no board data sent just send the usual webpage)
    return render_template('placement.html', BOARD_SIZE=BOARD_SIZE, ships=players['Human']['ships'])


@app.route('/attack')
def handle_attack() -> dict:
    """
    This handles When a user sends an attack
    :return: dictionary of the user and AI's guess boards and game status
    """

    message = ""  # The message we'll send to the web console

    user_coords = int(request.args.get('x')), int(request.args.get('y'))
    attack_status = gui_ext.attack_sunk(user_coords,
                                        players['AI']['board'],
                                        players['Human']['guess_board'],
                                        players['AI']['ships'])

    new_guess_board = gui_ext.update_guess_board(players['Human']['guess_board'],
                                                 user_coords,
                                                 players['AI']['board'],
                                                 attack_status)
    players['Human']['guess_board'] = new_guess_board

    # Send human guess details to console
    message += f'Player attacked {user_coords} and '
    if attack_status[0] == "hit":
        message += 'HIT'
    elif attack_status[0] == "sunk":
        message += 'SUNK'
    else:
        message += 'MISSED'

    # Generate attack and update guess board for the AI now
    ai_coords = mp_game_engine.generate_attack_ext(players['AI']['board'],
                                                   difficulty=AI_DIFFICULTY,
                                                   my_guess_board=players['AI']['guess_board'])
    attack_status = gui_ext.attack_sunk(ai_coords,
                                        players['Human']['board'],
                                        players['AI']['guess_board'],
                                        players['Human']['ships'])
    players['AI']['guess_board'] = gui_ext.update_guess_board(players['AI']['guess_board'],
                                                              ai_coords,
                                                              players['Human']['board'],
                                                              attack_status)

    # Add a message to the web console for the AI's guess
    message += f'<br> AI attacked {ai_coords} and '
    if attack_status[0] == "hit":
        message += 'HIT'
    elif attack_status[0] == "sunk":
        message += 'SUNK'
    else:
        message += 'MISSED'

    # Shift the AI and Human guess_boards and boards by the storm direction variable
    players['AI']['guess_board'] = storm_engine.shift(players['AI']['guess_board'], storm_direction)
    players['Human']['board'] = storm_engine.shift(players['Human']['board'], storm_direction)
    players['Human']['guess_board'] = storm_engine.shift(players['Human']['guess_board'],
                                                         storm_direction)
    players['AI']['board'] = storm_engine.shift(players['AI']['board'], storm_direction)

    response = {'my_guess_board': players['Human']['guess_board'],
                'opponent_guess_board': players['AI']['guess_board'],
                'message': message}

    if game_engine.count_ships_remaining(players['Human']['ships']) == 0:
        response['finished'] = 'The Human LOST! Better luck next time'
    elif game_engine.count_ships_remaining(players['AI']['ships']) == 0:
        response['finished'] = " The Human WON! Well done"

    return response


@app.route('/menu', methods=['POST'])
def handle_menu() -> dict | None:
    """
    When the return to menu button gets pressed this gets triggered. Stops the game
    :return: A dict just to show it completed fine
    """
    if request.method == 'POST':  # received the JSON data of a board set up
        global SET_BOARD
        global GAME_RUNNING
        SET_BOARD = False
        GAME_RUNNING = False

    return {'success': True}  # needs some JSON returned to show it worked


@app.route('/entry', methods=['POST'])
def entry_interface() -> dict | None:
    """
    When the Start game button gets pressed on the entry interface this gets triggered
    :return: dictionary to show it was received OK
    """
    if request.method == 'POST':  # received the JSON data of a board set up

        # Initialise the new game with the JSON data arguments
        json_data = json.loads(request.get_json())
        setup_game(int(json_data['board_size']),
                   json_data['stormy_mode'],
                   int(json_data['difficulty']))

    # It wants the data returned to it, so it can check transmission success
    return {'return': True}


@app.route('/')
def root() -> str:
    """
    Handles rendering all the webpages. If the game isn't started go to the entry page
    if its started but there's no board go to the placement page. Else the gameplay page
    :return: HTML web pages: either placement if the board needs to be set up or gameplay if it has
    """
    if GAME_RUNNING:
        if not SET_BOARD:  # If game started but no board set then go to placement page
            return render_template('placement_extended.html',
                                   board_size=BOARD_SIZE,
                                   ships=players['Human']['ships'])

        # Go to gameplay page
        return render_template('gameplay_extended.html',
                               opp_guess_board=players['AI']['guess_board'],
                               my_guess_board=players['Human']['guess_board'])

    # If game not started go to the menu page
    return render_template('entry.html')


def setup_game(board_size: int = 10, stormy: bool = False, ai_diff: int = 4) -> None:
    """
    Initialises a new game, resets boards etc.
    :param board_size: How big the board should be
    :param stormy: Is it stormy game-mode
    :param ai_diff: The AI difficulty level
    :return: None
    """

    global SET_BOARD
    SET_BOARD = False

    global GAME_RUNNING
    GAME_RUNNING = True

    global BOARD_SIZE
    BOARD_SIZE = board_size

    global AI_DIFFICULTY
    AI_DIFFICULTY = ai_diff

    global storm_direction
    if stormy:
        # Choose a random direction but not (0,0)
        storm_direction = (random.choice([-1, 1]), random.choice([-1, 1]))
    else:
        storm_direction = (0, 0)

    # Set up game
    global players
    players = {'Human': {'board': components.initialise_board(BOARD_SIZE),
                         'ships': components.create_battleships()},
               'AI': {'board': components.initialise_board(BOARD_SIZE),
                      'ships': components.create_battleships()}}

    players['AI']['board'] = components.place_battleships(players['AI']['board'],
                                                          players['AI']['ships'],
                                                          placement_method='random')

    players['Human']['guess_board'] = gui_ext.create_guess_board(players['AI']['board'])


if __name__ == '__main__':
    # Initialise variables needed globally
    SET_BOARD = False
    GAME_RUNNING = False
    storm_direction = (0, 0)
    BOARD_SIZE = 0
    AI_DIFFICULTY = 4
    players = {}
    app.run()
