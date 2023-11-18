"""
This is my main code for running a flask battleships game
Includes added extensions:
- Guessboards (holds move histories and can show ships sunk)
- all board processing is done in python and HTML is just sent a copy of
    guessboards  (Means HTML website is persistent)
- Has the storm mode
- Has an entry screen
- Has difficulty modes
- Game itself encapsulated in OO
"""

# Import flask libs
import random
import json
from flask import Flask
from flask import request
from flask import render_template

# Import gameplay libs
import game_engine
import mp_game_engine as mpg
import components
import gui_extensions as gui_ext
import storm_engine as storm

app = Flask(__name__)


class BattleshipsGame:
    """
   Encapsulated the battleships game functions into a class so we don't
   need to use global variables
   """

    def __init__(self):
        # Initialise the variables, they'll get set later on
        self.set_board = False
        self.game_running = False
        self.board_size = 10
        self.ai_difficulty = 4
        self.storm_direction = (0, 0)
        self.players = {}

    # FUNCTIONS FOR HANDLING THE START SCREEN
    def entry_interface(self) -> dict | None:
        """
        When the Start game button gets pressed on the entry interface this gets triggered
        It sets up a game with the data returned
        :return: dictionary to show it was received OK
        """
        if request.method == 'POST':  # received data to set up a game

            # Initialise the new game with the JSON data arguments
            json_data = json.loads(request.get_json())
            self.board_size = int(json_data['board_size'])
            self.ai_difficulty = int(json_data['difficulty'])

            # If its using stormy mode then set a direction
            if json_data['stormy_mode']:
                # Choose a random direction but not (0,0)
                self.storm_direction = (random.choice([-1, 1]), random.choice([-1, 1]))
            else:
                self.storm_direction = (0, 0)

            # Start the game but make sure the board isn't set
            self.game_running = True
            self.set_board = False

            # Reset the player dictionaries and create boards, ships etc
            self.players ={}
            self.players = {'Human': {'board': components.initialise_board(self.board_size),
                                      'ships': components.create_battleships()},
                            'AI': {'board': components.initialise_board(self.board_size),
                                   'ships': components.create_battleships()}}

            self.players['AI']['board'] = components.place_battleships(self.players['AI']['board'],
                                                                       self.players['AI']['ships'],
                                                                       placement_method='random')

            # Since the AI's board is created we can make the player's guess board
            new_guess_board = gui_ext.create_guess_board(self.players['AI']['board'])
            self.players['Human']['guess_board'] = new_guess_board

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

        return {'success': True}  # needs some JSON returned to show it worked

    # FUNCTIONS FOR GAMEPLAY
    def placement_interface(self) -> str:
        """
        This handles the placement menu, so when you first put your ships on the board
        :return: Returns a JSON file if it's a POST request, or the HTML webpage if it's not
        """
        if request.method == 'POST':  # received the JSON data of a board set up
            json_data = request.get_json()

            # so it can redirect to the main game page and start game
            self.set_board = True

            # Because we can only read a JSON ship data from file we need to save it then load it in
            with open("placement.json", "w", encoding="utf-8") as outfile:
                json.dump(json_data, outfile)

            new_board = components.place_battleships(self.players['Human']['board'],
                                                     self.players['Human']['ships'],
                                                     placement_method='custom')
            self.players['Human']['board'] = new_board

            # As we now have the player's board we can create the AI's guess_board
            new_guess_board = gui_ext.create_guess_board(self.players['Human']['board'])
            self.players['AI']['guess_board'] = new_guess_board

            # It wants the data returned to it, so it can check transmission success
            return json_data

        # If it's not a POST request (no board data sent just send the usual webpage)
        return render_template('placement.html', board_size=self.board_size,
                               ships=self.players['Human']['ships'])

    def handle_attack(self) -> dict:
        """
        This handles When a user sends an attack
        :return: dictionary of the user and AI's guess boards and game status
        """

        message = ""  # The message we'll send to the web console

        # Get the user coordinates
        user_coords = int(request.args.get('x')), int(request.args.get('y'))

        # Get the result of the user's attack and update the user's guess board
        attack_status = gui_ext.attack_sunk(user_coords,
                                            self.players['AI']['board'],
                                            self.players['Human']['guess_board'],
                                            self.players['AI']['ships'])

        new_guess_board = gui_ext.update_guess_board(self.players['Human']['guess_board'],
                                                     user_coords,
                                                     self.players['AI']['board'],
                                                     attack_status)
        self.players['Human']['guess_board'] = new_guess_board

        # Send human guess details to console
        message += f'Player attacked {user_coords} and '
        if attack_status[0] == "hit":
            message += 'HIT'
        elif attack_status[0] == "sunk":
            message += 'SUNK'
        else:
            message += 'MISSED'

        # Generate attack location for the AI according to difficulty level
        ai_coords = mpg.generate_attack_ext(self.players['AI']['board'],
                                            difficulty=self.ai_difficulty,
                                            my_guess_board=self.players['AI']['guess_board'])
        # Get the result of the AI's attack and update its guess board
        attack_status = gui_ext.attack_sunk(ai_coords,
                                            self.players['Human']['board'],
                                            self.players['AI']['guess_board'],
                                            self.players['Human']['ships'])
        new_guess_board = gui_ext.update_guess_board(self.players['AI']['guess_board'],
                                                     ai_coords,
                                                     self.players['Human']['board'],
                                                     attack_status)
        self.players['AI']['guess_board'] = new_guess_board

        # Add a message to the web console for the AI's guess
        message += f'<br> AI attacked {ai_coords} and '
        if attack_status[0] == "hit":
            message += 'HIT'
        elif attack_status[0] == "sunk":
            message += 'SUNK'
        else:
            message += 'MISSED'

        # Shift the AI and Human guess_boards and boards by the storm_direction variable
        # The storm_direction will be (0,0) if no storm
        self.players['AI']['guess_board'] = storm.shift(self.players['AI']['guess_board'],
                                                        self.storm_direction)
        self.players['Human']['board'] = storm.shift(self.players['Human']['board'],
                                                     self.storm_direction)
        self.players['Human']['guess_board'] = storm.shift(self.players['Human']['guess_board'],
                                                           self.storm_direction)
        self.players['AI']['board'] = storm.shift(self.players['AI']['board'],
                                                  self.storm_direction)

        # Return the response to the HTML interface with both user's guess boards,
        #  console log and finish status if required
        response = {'my_guess_board': self.players['Human']['guess_board'],
                    'opponent_guess_board': self.players['AI']['guess_board'],
                    'message': message}

        if game_engine.count_ships_remaining(self.players['Human']['ships']) == 0:
            response['finished'] = 'The Human LOST! Better luck next time'
        elif game_engine.count_ships_remaining(self.players['AI']['ships']) == 0:
            response['finished'] = " The Human WON! Well done"

        return response

    def root(self) -> str:
        """
        Handles rendering all the webpages. If the game isn't started go to the entry page
        if its started but there's no board go to the placement page. Else the gameplay page
        :return: HTML web pages: either placement if the board needs to be set up or gameplay
         if it has
        """
        if self.game_running:
            if not self.set_board:  # If game started but no board set then go to placement page
                return render_template('placement_extended.html',
                                       board_size=self.board_size,
                                       ships=self.players['Human']['ships'])

            # Go to gameplay page If game running and board set
            return render_template('gameplay_extended.html',
                                   opp_guess_board=self.players['AI']['guess_board'],
                                   my_guess_board=self.players['Human']['guess_board'])

        # If game not started go to the menu page
        return render_template('entry.html')


# The functions below handle the interactions between flask requests
# and the BattleshipsGame class' functions

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface() -> str:
    """
    returns the game instance's placement_interface function
    :return: Returns a JSON file if it's a POST request, or the HTML webpage if it's not
    """
    return game.placement_interface()


@app.route('/attack')
def handle_attack() -> dict:
    """
    returns the game instance's handle_attack function result
    :return: The status of the user's attack and where the AI fired back
    """
    return game.handle_attack()


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


BOARD_SIZE = 10

game = BattleshipsGame()

if __name__ == '__main__':
    app.run()
