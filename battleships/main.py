"""
This module runs the main battleships game
"""

import os
import json
from copy import deepcopy
import logging
from flask import Flask, request, render_template

# Import battleships libs, pycharm likes it one way, terminal likes it the other
# using this try except bit here makes it work either way round
try:
    from battleships import game_engine
    from battleships import components
    from battleships import advanced_ai as ai
except ImportError:
    import game_engine
    import components
    import advanced_ai as ai

app = Flask(__name__)

# Set up the logging
logging.basicConfig(filename='log', level=logging.DEBUG,
                    format='%(asctime)s-%(levelname)s-%(message)s', filemode='a')
logging.getLogger().addHandler(logging.StreamHandler())


class BattleshipsGame:
    """
    Encapsulated the battleships game functions into a class so we don't
    need to use global variables
    """

    def __init__(self):
        self.set_board = False
        self.game_running = False
        self.board_size = 10
        self.ai_difficulty = 4
        self.stormy = False
        self.players = {}

    def entry_interface(self) -> dict | None:
        """
        When the Start game button gets pressed on the entry interface this gets triggered
        It sets up a game with the data returned

        :return: dictionary to show it was received OK
        """
        if request.method == 'POST':  # received data to set up a game

            app.logger.info('Just loaded into the placement interface')

            # Initialise the new game with the JSON data arguments
            json_data = json.loads(request.get_json())
            self.board_size = int(json_data['board_size'])
            self.ai_difficulty = int(json_data['difficulty'])
            self.stormy = bool(json_data['stormy_mode'])

            # Start the game but make sure the board isn't set
            self.game_running = True
            self.set_board = False
            # Reset the player dictionaries and create boards, ships etc
            self.players = {'Human': {'board': components.initialise_board(self.board_size),
                                      'ships': components.create_battleships(),
                                      'history': []},
                            'AI': {'board': components.initialise_board(self.board_size),
                                   'ships': components.create_battleships(),
                                   'history': []}}

            self.players['AI']['board'] = components.place_battleships(self.players['AI']['board'],
                                                                       self.players['AI']['ships'],
                                                                       algorithm='random')
            # Now AI has made its board lets save the original board so we can keep track
            # of what's sunk and where
            self.players['AI']['original_board'] = deepcopy(self.players['AI']['board'])

        # It wants the data returned to it, so it can check transmission success
        return {'return': True}

    def handle_menu(self) -> dict | None:
        """
        When the return to menu button gets pressed this gets triggered. Just stops the game
        and will return to the entry screen

        :return: A dict just to show it completed fine
        """
        if request.method == 'POST':  # received the JSON data of a board set up
            self.set_board = False
            self.game_running = False
            app.logger.info('Gone back to main menu')

        return {'success': True}  # needs some JSON returned to show it worked

    def placement_interface(self) -> str:
        """
        This handles the placement menu, so when you first put your ships on the board

        :return: Returns a JSON file if it's a POST request, or the HTML webpage if it's not
        """
        if request.method == 'POST':  # received the JSON data of a board set up
            json_data = request.get_json()
            app.logger.info('Just received placement ship data')

            # Because we can only read a JSON ship data from file we need to save it then load it in

            # recreate placement.json filename using absolute path
            new_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'placement.json')
            with open(new_path, "w", encoding="utf-8") as outfile:
                json.dump(json_data, outfile)

            new_layout = components.place_battleships(self.players['Human']['board'],
                                                      self.players['Human']['ships'],
                                                      algorithm='custom')

            self.players['Human']['board'] = new_layout
            self.players['Human']['original_board'] = deepcopy(new_layout)

            # so it can redirect to the main game page and start game
            self.set_board = True

            # It wants the data returned to it, so it can check transmission success
            return json_data

        # If it's not a POST request (no board data sent just send the usual webpage)
        return render_template('placement.html',
                               board_size=self.board_size,
                               ships=self.players['Human']['ships'])

    def process_attack(self) -> dict:
        """
        This handles When a user sends an attack

        :return: The status of the user's attack and where the AI fired back
        """

        app.logger.info('Now processing player attack')

        # Deal with the human attack
        valid_coordinate = False
        try:
            user_coords = int(request.args.get('x')), int(request.args.get('y'))
            if (0 <= user_coords[0] < len(self.players['AI']['board']) and
                    0 <= user_coords[1] < len(self.players['AI']['board'])):
                valid_coordinate = True
            app.logger.info(' user guesses %s',user_coords)

        except ValueError:
            user_coords = (0, 0)
            app.logger.warning('User tried to enter invalid coordinates')

        if valid_coordinate:  # If we didn't enter valid coordinates then assume we missed
            attack_status = game_engine.attack(user_coords, self.players['AI']['board'],
                                               self.players['AI']['ships'])
            self.players['Human']['history'].append(user_coords)
        else:
            attack_status = False

        # Calculate which of the AI ships we have sunk based on its original board
        ai_sunken_places = components.get_sunken_ships(self.players['AI'])

        # The AI's attack
        ai_coords = ai.generate_advanced_attack(self.ai_difficulty,
                                                self.players['Human'],
                                                self.players['AI']['history'])
        game_engine.attack(ai_coords, self.players['Human']['board'],
                           self.players['Human']['ships'])
        self.players['AI']['history'].append(ai_coords)
        app.logger.info('ai guessed %s', ai_coords)

        # Calculate which of my ships the AI has sunk based on my original board
        my_sunken_places = components.get_sunken_ships(self.players['Human'])

        # Send back return data to the Front end
        return_data = {'hit': attack_status, 'AI_Turn': ai_coords,
                       'sunk': [ai_sunken_places, my_sunken_places]}

        # bool of whether game is finished
        finished = (game_engine.count_ships_remaining(self.players['Human']['ships']) == 0 or
                    game_engine.count_ships_remaining(self.players['AI']['ships']) == 0)
        if finished:
            ai_won = game_engine.count_ships_remaining(self.players['Human']['ships']) == 0
            return_data['finished'] = f"The Human {'LOST' if ai_won else 'WON'}! Game over"
            app.logger.info("The Human %s! Game over", 'LOST' if ai_won else 'WON')

        return return_data

    def root(self) -> str:
        """
        Handles the main gameplay webpage, if game isn't set up then it goes
        to the placement page

        :return: HTML web pages: either placement if the board needs to be set up
         or gameplay if it has already
        """

        if self.game_running:
            if not self.set_board:  # If game started but no board set then go to placement page
                return render_template('placement.html',
                                       board_size=self.board_size,
                                       ships=self.players['Human']['ships'])

            # Go to gameplay page If game running and board set
            return render_template('main.html',
                                   player_board=self.players['Human']['board'],
                                   stormy = self.stormy)

        # If game not started go to the menu page
        return render_template('entry.html')


@app.route('/placement', methods=['GET', 'POST'])
def placement_interface() -> str:
    """
    returns the game instance's placement_interface function

    :return: Returns a JSON file if it's a POST request, or the HTML webpage if it's not
    """
    return game.placement_interface()


@app.route('/attack')
def process_attack() -> dict:
    """
    returns the game instance's handle_attack function

    :return: The status of the user's attack and where the AI fired back
    """
    return game.process_attack()


@app.route('/menu', methods=['POST'])
def handle_menu() -> dict:
    """
    Returns the game instance's handle_menu function result

    :return: The dictionary result to respond that the handle_menu function worked
    """
    return game.handle_menu()


@app.route('/entry', methods=['POST'])
def entry_interface() -> dict:
    """
    Returns the game instance's entry_interface function result

    :return: The dictionary result to respond that the entry_interface function worked
    """
    return game.entry_interface()


@app.route('/')
def root() -> str:
    """
    returns the game instance's root function

    :return: HTML web pages: either placement if the board needs to be set up
    or gameplay if it has already
    """

    return game.root()


game = BattleshipsGame()

if __name__ == '__main__':
    # Set up game

    app.logger.debug("This is an info message.")
    app.run()
