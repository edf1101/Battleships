"""
This module runs a simple Battleships game with no extensions (albeit using OOP)
"""

import json
from flask import Flask
from flask import request
from flask import render_template

# Import gameplay libs
import game_engine
import mp_game_engine
import components

app = Flask(__name__)


class BattleshipsGame:
    """
    Encapsulated the battleships game functions into a class so we don't
    need to use global variables
    """

    def __init__(self, board_size):
        self.players = {}
        self.set_board = False
        self.board_size = board_size
        self.players['Human'] = {'board': components.initialise_board(self.board_size),
                                 'ships': components.create_battleships()}
        self.players['AI'] = {'board': components.initialise_board(self.board_size),
                              'ships': components.create_battleships()}

        self.players['AI']['board'] = components.place_battleships(self.players['AI']['board'],
                                                                   self.players['AI']['ships'],
                                                                   placement_method='random')

    def placement_interface(self) -> str:
        """
        This handles the placement menu, so when you first put your ships on the board
        :return: Returns a JSON file if it's a POST request, or the HTML webpage if it's not
        """
        if request.method == 'POST':  # received the JSON data of a board set up
            json_data = request.get_json()

            # Because we can only read a JSON ship data from file we need to save it then load it in
            with open("placement.json", "w", encoding="utf-8") as outfile:
                json.dump(json_data, outfile)

            new_layout = components.place_battleships(self.players['Human']['board'],
                                                      self.players['Human']['ships'],
                                                      placement_method='custom')
            self.players['Human']['board'] = new_layout

            # so it can redirect to the main game page and start game
            self.set_board = True

            # It wants the data returned to it, so it can check transmission success
            return json_data

        # If it's not a POST request (no board data sent just send the usual webpage)
        return render_template('placement.html',
                               board_size=self.board_size,
                               ships=self.players['Human']['ships'])

    def handle_attack(self) -> str:
        """
        This handles When a user sends an attack
        :return: The status of the user's attack and where the AI fired back
        """

        user_coords = int(request.args.get('x')), int(request.args.get('y'))
        attack_status = game_engine.attack(user_coords, self.players['AI']['board'],
                                           self.players['AI']['ships'])

        ai_coords = mp_game_engine.generate_attack(self.players['AI']['board'])
        attack_status = game_engine.attack(ai_coords, self.players['Human']['board'],
                                           self.players['Human']['ships'])

        # Check to see if game over
        finished = (game_engine.count_ships_remaining(self.players['Human']['ships']) == 0 or
                    game_engine.count_ships_remaining(self.players['AI']['ships']) == 0)
        if finished:
            # Check who died
            if game_engine.count_ships_remaining(self.players['Human']['ships']) == 0:
                return {'hit': attack_status, 'AI_Turn': ai_coords,
                        'finished': " The Human LOST! Better luck next time"}
            return {'hit': attack_status, 'AI_Turn': ai_coords,
                    'finished': " The Human WON! Well done"}

        return {'hit': attack_status, 'AI_Turn': ai_coords}

    def root(self) -> str:
        """
        Handles the main gameplay webpage, if game isn't set up then it goes
        to the placement page
        :return: HTML web pages: either placement if the board needs to be set up
         or gameplay if it has already
        """
        if not self.set_board:
            return render_template('placement.html',
                                   board_size=self.board_size,
                                   ships=self.players['Human']['ships'])

        return render_template('gameplay.html',
                               player_board=self.players['Human']['board'])


@app.route('/placement', methods=['GET', 'POST'])
def placement_interface() -> str:
    """
    returns the game instance's placement_interface function
    :return: Returns a JSON file if it's a POST request, or the HTML webpage if it's not
    """
    return game.placement_interface()


@app.route('/attack')
def handle_attack() -> str:
    """
    returns the game instance's handle_attack function
    :return: The status of the user's attack and where the AI fired back
    """
    return game.handle_attack()


@app.route('/')
def root() -> str:
    """
    returns the game instance's root function
    :return: HTML web pages: either placement if the board needs to be set up
    or gameplay if it has already
    """
    return game.root()


BOARD_SIZE = 10
game = BattleshipsGame(BOARD_SIZE)

if __name__ == '__main__':
    # Set up game

    app.run()
