# Import flask libs
from flask import Flask
from flask import request
from flask import render_template

# Import gameplay libs
import game_engine
import mp_game_engine
import components

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

        # Because we can only read a JSON ship data from file we need to save it then load it in
        with open("placement.json", "w") as outfile:
            json.dump(json_data, outfile)
        players['Human']['board'] = components.place_battleships(players['Human']['board'], players['Human']['ships'],
                                                                 placement_method='custom')
        global set_board
        set_board = True  # so it can redirect to the main game page and start game (outer scope so use global)
        return json_data  # It wants the data returned to it, so it can check transmission success

    # If it's not a POST request (no board data sent just send the usual webpage)
    return render_template('placement.html', board_size=board_size, ships=players['Human']['ships'])


@app.route('/attack')
def handle_attack():
    """
    This handles When a user sends an attack
    :return: The status of the user's attack and where the AI fired back
    """

    user_coords = int(request.args.get('x')), int(request.args.get('y'))
    attack_status = game_engine.attack(user_coords, players['AI']['board'], players['AI']['ships'])

    ai_coords = mp_game_engine.generate_attack(players['AI']['board'])

    # Check to see if game over
    finished = (game_engine.count_ships_remaining(players['Human']['ships']) == 0 or
                game_engine.count_ships_remaining(players['AI']['ships']) == 0)
    if finished:
        # Check who died
        if game_engine.count_ships_remaining(players['Human']['ships']) == 0:
            return {'hit': attack_status, 'AI_Turn': ai_coords, 'finished': " The Human LOST! Better luck next time"}
        else:
            return {'hit': attack_status, 'AI_Turn': ai_coords, 'finished': " The Human WON! Well done"}

    return {'hit': attack_status, 'AI_Turn': ai_coords}


@app.route('/')
def root():
    """
    Handles the main gameplay webpage, unless the game isn't set up then it goes to the placement page
    :return: HTML web pages: either placement if the board needs to be set up or gameplay if it has
    """
    if not set_board:
        return render_template('placement.html',
                               board_size=board_size,
                               ships=players['Human']['ships'])
    else:
        return render_template('gameplay.html',
                               player_board=players['Human']['board'])


if __name__ == '__main__':
    players = {}
    set_board = False
    board_size = 10
    # Set up game
    players['Human'] = {'board': components.initialise_board(board_size), 'ships': components.create_battleships()}
    players['AI'] = {'board': components.initialise_board(board_size), 'ships': components.create_battleships()}

    players['AI']['board'] = components.place_battleships(players['AI']['board'], players['AI']['ships'],
                                                          placement_method='random')

    app.run()
