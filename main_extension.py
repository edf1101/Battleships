# Import flask libs
import random

from flask import Flask
from flask import request
from flask import render_template

# Import gameplay libs
import game_engine
import mp_game_engine
import components
import gui_extensions
import storm_engine

# Import other libs
import json

app = Flask(__name__)


@app.route('/placement', methods=['GET', 'POST'])
def placement_interface() -> str:
    """
    This handles the placement menu, so when you first put your ships on the board
    :return: Returns a JSON file if it's a POST request, or the HTML webpage if it's not
    """
    if request.method == 'POST':  # received the JSON data of a board set up
        json_data = request.get_json()

        global set_board
        set_board = True  # so it can redirect to the main game page and start game (outer scope so use global)

        # Because we can only read a JSON ship data from file we need to save it then load it in
        with open("placement.json", "w") as outfile:
            json.dump(json_data, outfile)
        players['Human']['board'] = components.place_battleships(players['Human']['board'], players['Human']['ships'],
                                                                 placement_method='custom')
        # Start the AI's Guess board
        players['AI']['guess_board'] = gui_extensions.create_guess_board(players['Human']['board'])

        return json_data  # It wants the data returned to it, so it can check transmission success

    # If it's not a POST request (no board data sent just send the usual webpage)
    return render_template('placement.html', board_size=board_size, ships=players['Human']['ships'])


@app.route('/attack')
def handle_attack() -> str:
    """
    This handles When a user sends an attack
    :return: The status of the user's attack and where the AI fired back
    """

    message = ""  # The message we'll send to the web console

    user_coords = int(request.args.get('x')), int(request.args.get('y'))
    attack_status = gui_extensions.attack_sunk(user_coords,
                                               players['AI']['board'],
                                               players['Human']['guess_board'],
                                               players['AI']['ships'])

    players['Human']['guess_board'] = gui_extensions.update_guess_board(players['Human']['guess_board'],
                                                                        user_coords,
                                                                        players['AI']['board'],
                                                                        attack_status)

    message += f'Player attacked {user_coords} and '  # Send human guess details to console
    message += f'{"HIT" if attack_status[0] == "hit" else "SUNK" if attack_status[0] == "sunk" else "MISSED"}'

    # Generate attack and update guess board for the AI now
    ai_coords = mp_game_engine.generate_attack_ext(players['AI']['board'],
                                                   difficulty=ai_difficulty,
                                                   my_guess_board=players['AI']['guess_board'])
    attack_status = gui_extensions.attack_sunk(ai_coords,
                                               players['Human']['board'],
                                               players['AI']['guess_board'],
                                               players['Human']['ships'])
    players['AI']['guess_board'] = gui_extensions.update_guess_board(players['AI']['guess_board'],
                                                                     ai_coords,
                                                                     players['Human']['board'],
                                                                     attack_status)

    # Add a message to the web console for the AI's guess
    message += f'<br> AI attacked {ai_coords} and '
    message += f'{"HIT" if attack_status[0] == "hit" else "SUNK" if attack_status[0] == "sunk" else "MISSED"}'

    # Shift the AI and Human guess_boards and boards by the storm direction variable
    players['AI']['guess_board'] = storm_engine.shift(players['AI']['guess_board'], storm_direction)
    players['Human']['board'] = storm_engine.shift(players['Human']['board'], storm_direction)
    players['Human']['guess_board'] = storm_engine.shift(players['Human']['guess_board'], storm_direction)
    players['AI']['board'] = storm_engine.shift(players['AI']['board'], storm_direction)

    response = {'my_guess_board': players['Human']['guess_board'],
                'opponent_guess_board': players['AI']['guess_board'],
                'message': message}

    if game_engine.count_ships_remaining(players['Human']['ships']) == 0:
        response['finished'] = 'The Human LOST! Better luck next time'
    elif game_engine.count_ships_remaining(players['AI']['ships']) == 0:
        response['finished'] = " The Human WON! Well done"

    return response


@app.route('/menu', methods=['GET', 'POST'])
def handle_menu() -> dict:
    if request.method == 'POST':  # received the JSON data of a board set up
        json_data = json.dumps(request.get_json())
        global set_board
        global game_running
        set_board = False
        game_running = False
        return {'success': True}  # needs some JSON returned to show it worked


@app.route('/entry', methods=['GET', 'POST'])
def entry_interface():
    print('entry')
    if request.method == 'POST':  # received the JSON data of a board set up
        json_data = json.loads(request.get_json())

        setup_game(int(json_data['board_size']), json_data['stormy_mode'], int(json_data['difficulty']))

        return {'return': True}  # It wants the data returned to it, so it can check transmission success

    # If it's not a POST request (no board data sent just send the usual webpage)
    return render_template('entry.html')


@app.route('/')
def root() -> str:
    """
    Handles the main gameplay webpage, unless the game isn't set up then it goes to the placement page
    :return: HTML web pages: either placement if the board needs to be set up or gameplay if it has
    """
    if game_running:
        if not set_board:
            return render_template('placement_extended.html',
                                   board_size=board_size,
                                   ships=players['Human']['ships'])
        else:
            return render_template('gameplay_extended.html',
                                   opp_guess_board=players['AI']['guess_board'],
                                   my_guess_board=players['Human']['guess_board'])
    else:
        return render_template('entry.html')


def setup_game(board_size_argument: int = 10, stormy: bool = False, ai_diff: int = 4) -> None:
    """
    Initialises a new game, resets boards etc.
    :param board_size_argument: How big the board should be
    :param stormy: Is it stormy game-mode
    :param ai_diff: The AI difficulty level
    :return: None
    """

    global set_board
    set_board = False

    global game_running
    game_running = True

    global board_size
    board_size = board_size_argument

    global ai_difficulty
    ai_difficulty = ai_diff

    global storm_direction
    if stormy:
        storm_direction = (random.randrange(-1, 2), random.randrange(-1, 2))  # Random between -1,1 in x&y
    else:
        storm_direction = (0, 0)

    # Set up game
    global players
    players = {'Human': {'board': components.initialise_board(board_size),
                         'ships': components.create_battleships()},
               'AI': {'board': components.initialise_board(board_size),
                      'ships': components.create_battleships()}}

    players['AI']['board'] = components.place_battleships(players['AI']['board'], players['AI']['ships'],
                                                          placement_method='random')

    players['Human']['guess_board'] = gui_extensions.create_guess_board(players['AI']['board'])


if __name__ == '__main__':
    # Initialise variables needed globally
    set_board = False
    game_running = False
    storm_direction = (0, 0)
    board_size = 0
    ai_difficulty = 4
    players = {}
    app.run()
