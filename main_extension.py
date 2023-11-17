# Import flask libs
from flask import Flask
from flask import request
from flask import render_template

# Import gameplay libs
import game_engine
import mp_game_engine
import components
import gui_extensions

# Import other libs
import json

app = Flask(__name__)


@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
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
def handle_attack():
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
                                                   difficulty=4,
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

    response = {'my_guess_board': players['Human']['guess_board'],
                'opponent_guess_board': players['AI']['guess_board'],
                'message': message}

    if game_engine.count_ships_remaining(players['Human']['ships']) == 0:
        response['finished'] = 'The Human LOST! Better luck next time'
    elif game_engine.count_ships_remaining(players['AI']['ships']) == 0:
        response['finished'] = " The Human WON! Well done"

    return response


@app.route('/')
def root():
    """
    Handles the main gameplay webpage, unless the game isn't set up then it goes to the placement page
    :return: HTML web pages: either placement if the board needs to be set up or gameplay if it has
    """
    if not set_board:
        return render_template('placement_extended.html',
                               board_size=board_size,
                               ships=players['Human']['ships'])
    else:
        return render_template('gameplay_extended.html',
                               opp_guess_board=players['AI']['guess_board'],
                               my_guess_board=players['Human']['guess_board'])


if __name__ == '__main__':
    players = {}
    set_board = False
    board_size = 10
    # Set up game
    players['Human'] = {'board': components.initialise_board(board_size),
                        'ships': components.create_battleships()}
    players['AI'] = {'board': components.initialise_board(board_size),
                     'ships': components.create_battleships()}

    players['AI']['board'] = components.place_battleships(players['AI']['board'], players['AI']['ships'],
                                                          placement_method='random')

    players['Human']['guess_board'] = gui_extensions.create_guess_board(players['AI']['board'])

    app.run()
