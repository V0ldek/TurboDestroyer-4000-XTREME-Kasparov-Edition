#####
# This module contains all the logic regarding management of the board:
# processing moves, checking victory conditions, etc.
#####

from Board import Board

# The one and only current game board
_board = Board()

# Previous board for undoing a move
_prev_board = Board()
_undo_available = False


def get_board():
    """ Returns the Board object. Creates an empty board if it didn't exist
    """

    global _board

    if _board is None:
        _board = Board()

    return _board


def process_move(move, player):
    """ Checks whether the Player's move is valid or not,
    returns False if it is not, otherwise it updates the board accordingly
    and returns True
    """

    global _board
    global _prev_board
    global _undo_available

    # Prepare the move for possible undo
    _prev_board = _board.copy()
    _undo_available = True

    if _board.is_move_legal(move):
        _board = _board.make_move(move, player)
        return True
    else:
        return False


def check_game_over():
    """ Checks the board for victory conditions
    """

    return _board.check_game_over()


def undo_move():
    """ Undoes one and only one move. Only one move is stored to undo.
    """
    global _board

    if not _undo_available:
        return

    _board = _prev_board.copy()


def reset():
    """ Sets the board to a completely new and empty one
    """

    global _board

    _board = Board()
