#####
# This module is responsible for managing the flow of the program, telling
# other modules what to do. It contains the main game loop
#####

import datetime
import math
from connectfour import AIManager
from connectfour import LevelManager
from connectfour import UserInterface
from connectfour.GameplayStatics import *
        
if DEBUG:
    f = open("gamelog" + str(datetime.datetime.now().time().hour) + " " + str(datetime.datetime.now().time().minute) +
         " " + str(datetime.datetime.now().time().second) + '.txt', 'w')

ai_wins = 0
player_wins = 0
draws = 0


def handle_move(move):
    """ Instructs all necessary modules to process given move
    """
    global ai_wins
    global player_wins
    global draws

    # Handle a reset move
    if move == MOVE_RESET:
        UserInterface.reset()
        LevelManager.reset()
        return

    # Handle an undo move
    if move == MOVE_UNDO:
        UserInterface.undo_move()
        LevelManager.undo_move()
        LevelManager.get_board().print_board(f)
        return

    # Find the row into which the piece was placed
    row = LevelManager.get_board().get_counter(move) - 1

    # Tell the UserInterface to update all graphics
    UserInterface.handle_move(move, row)

    # Print the board to stdout
    if DEBUG:
        LevelManager.get_board().print_board(f)

    # Tell the LevelManager to check for victory conditions
    outcome = LevelManager.check_game_over()

    # Tell UserInterface to handle game over if it occurred
    if outcome != OUTCOME_NOTHING:
        if outcome == OUTCOME_PLAYER:
            player_wins += 1
        elif outcome == OUTCOME_AI:
            ai_wins += 1
        elif outcome == OUTCOME_DRAW:
            draws += 1

        if DEBUG:
            f.write("PLAYER: " + str(player_wins) + " AI: " + str(ai_wins) + " DRAWS: " + str(draws) + "\n")

        UserInterface.handle_game_over(outcome)
        LevelManager.reset()
        AIManager.reset()
        return


def main_loop():
    """ The main game loop controlling the game cycle
    """

    # Startup the graphics engine
    UserInterface.startup(PLAYER)

    # Create the board for the first time
    LevelManager.get_board()

    # Whether the second player is AI
    versus_ai = True

    # Whether the first player is AI
    ai_versus = False

    while not UserInterface.is_exiting():

        if DEBUG:
            print "board's hash = " + str(LevelManager.get_board().hash)

        if UserInterface.get_current_player() == PLAYER:
            # Get and process the Player's input
            if ai_versus:
                # Get an AI move
                player_input = AIManager.make_alpha_beta_move(LevelManager.get_board(), AIManager.basic_evaluate,
                                                              PLAYER)
            else:
                # Read player's input
                player_input = UserInterface.get_input()

            # Make sure we were given a legal move to perform,
            # if not, tell the UI to inform the user about it and ask again
            while player_input != MOVE_RESET and player_input != MOVE_UNDO and \
                    (player_input == MOVE_ILLEGAL or not LevelManager.process_move(player_input, PLAYER)):

                if UserInterface.is_exiting():
                    return

                UserInterface.handle_illegal_move()

                if ai_versus:
                    # AI can't make an illegal move
                    print "AI tried to make an illegal move"
                    raise RuntimeError
                else:
                    player_input = UserInterface.get_input()

            # Handle the move, since it's legal
            handle_move(player_input)
        else:

            if versus_ai:
                # Get an AI move'''ai_move = AIManager.make_monte_carlo_move(LevelManager.get_board(), AIManager.basic_evaluate'''                                                             PLAYER, math.sqrt(2))
                ai_move = AIManager.make_alpha_beta_move(LevelManager.get_board(), AIManager.basic_evaluate,
                                                         AI)
            else:
                # Read player's input
                ai_move = UserInterface.get_input()

            while ai_move != MOVE_RESET and ai_move != MOVE_UNDO and \
                    (ai_move == MOVE_ILLEGAL or not LevelManager.process_move(ai_move, AI)):
        
                if UserInterface.is_exiting():
                    return
        
                UserInterface.handle_illegal_move()
        
                if versus_ai:
                    # AI can't make an illegal move
                    if DEBUG:
                        print "AI tried to make an illegal move"
                    
                    raise RuntimeError
                else:
                    ai_move = UserInterface.get_input()

            handle_move(ai_move)

