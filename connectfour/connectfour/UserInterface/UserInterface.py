#####
# This module handles displaying information on the screen, as well as getting the user's input
#####

from graphics import *

from connectfour.GameplayStatics import *

# The one and only game window
_window = None

# The game window's dimensions
WINDOW_SIZE_X = 1280
WINDOW_SIZE_Y = 720

# Position and dimensions for the move indicator rectangle
MOVE_INDICATOR_POS_X = 970
MOVE_INDICATOR_POS_Y = 215
MOVE_INDICATOR_SIZE_X = 200
MOVE_INDICATOR_SIZE_Y = 200

# Values for pieces display
CIRCLE_RADIUS = 50
CIRCLE_Y_OFFSET = 466

FONT_SIZE = 36

# The move indicator rectangle
_move_indicator = None

# External images
_numbers_image = None

# List for all circles drawn on screen
_circles_list = []

# Who is the player that starts the game
_starting_player = PLAYER

# Who is the current player
_current_player = PLAYER

# Whether or not we can undo a move
_undo_available = False

# Colors
PLAYER_COLOR = color_rgb(255, 51, 51)
PLAYER_WIN_COLOR = color_rgb(200, 25, 25)
AI_COLOR = color_rgb(0, 128, 255)
AI_WIN_COLOR = color_rgb(0, 64, 128)
DRAW_COLOR = color_rgb(128, 90, 153)
COLUMN_INDICATOR_COLOR = color_rgb(255, 153, 51)
BACKGROUND_COLOR = color_rgb(100, 100, 100)

# Key binds
KEY_BIND_RESET = 'r'
KEY_BIND_UNDO = ''


def set_move(current):
    """ Change the current player to the given one
    """
    global _current_player
    global _move_indicator

    _current_player = current

    # Update the move indicator rectangle
    if current == PLAYER:
        _move_indicator.setFill(PLAYER_COLOR)
    elif current == AI:
        _move_indicator.setFill(AI_COLOR)
    else:
        # If current is not a valid player, freak out
        print "Wrong parameter passed to UserInterface.set_move(current)"
        raise RuntimeError


def startup(starting_player):
    """ Called once at program startup. Creates the game window and the graphics that are permanently on the screen
    """
    global _window
    global _starting_player
    global _move_indicator
    global _numbers_image

    # Create the game window
    _window = GraphWin("Connect4", WINDOW_SIZE_X, WINDOW_SIZE_Y)
    _window.setBackground(BACKGROUND_COLOR)

    # Create the move indicator rectangle
    _move_indicator = Rectangle(Point(MOVE_INDICATOR_POS_X, MOVE_INDICATOR_POS_Y),
                                Point(MOVE_INDICATOR_POS_X + MOVE_INDICATOR_SIZE_X,
                                      MOVE_INDICATOR_POS_Y + MOVE_INDICATOR_SIZE_Y))

    # Set the starting player
    _starting_player = starting_player
    set_move(starting_player)

    # Draw everything we've just created onto the screen
    _move_indicator.draw(_window)

    # Create indicators for columns
    for i in range(NUMBER_OF_COLUMNS):
        circle = Circle(Point((i + 2) * 2 * CIRCLE_RADIUS, CIRCLE_Y_OFFSET - (-2) * 2 * CIRCLE_RADIUS), CIRCLE_RADIUS)
        circle.setFill(COLUMN_INDICATOR_COLOR)
        circle.draw(_window)

    # Horizontal grid lines
    for i in range(NUMBER_OF_ROWS + 1):
        line = Line(Point(3 * CIRCLE_RADIUS, i * 2 * CIRCLE_RADIUS + CIRCLE_Y_OFFSET - 9 * CIRCLE_RADIUS),
                    Point(NUMBER_OF_COLUMNS * 2 * CIRCLE_RADIUS + 3 * CIRCLE_RADIUS,
                          i * 2 * CIRCLE_RADIUS + CIRCLE_Y_OFFSET - 9 * CIRCLE_RADIUS))
        line.draw(_window)

    # Vertical grid lines
    for i in range(NUMBER_OF_COLUMNS + 1):
        line = Line(Point((i + 2) * 2 * CIRCLE_RADIUS - CIRCLE_RADIUS, CIRCLE_Y_OFFSET + 3 * CIRCLE_RADIUS),
                    Point((i + 2) * 2 * CIRCLE_RADIUS - CIRCLE_RADIUS,
                          CIRCLE_Y_OFFSET - NUMBER_OF_ROWS * 2 * CIRCLE_RADIUS + 3 * CIRCLE_RADIUS))
        line.draw(_window)

    # Numbers for column indicators
    for i in range(NUMBER_OF_COLUMNS):
        text = Text(Point((i + 2) * 2 * CIRCLE_RADIUS, CIRCLE_Y_OFFSET + 4 * CIRCLE_RADIUS), i + 1)
        text.setSize(FONT_SIZE)
        text.draw(_window)

    text = Text(Point(WINDOW_SIZE_X - 120, WINDOW_SIZE_Y - 20), str('version Alpha 1.5')).draw(_window)
    text.setSize(20)


def reset():
    """ Reset the graphics to a freshly started game state
    """

    # Delete all the pieces from the screen
    for circle in _circles_list:
        circle.undraw()

    # Get back to the starting player
    set_move(_starting_player)


def get_input():
    """ Reads the Player's keyboard input and returns a move
    """

    key = _window.getKey()

    # Check the key binds and move legality
    if key == KEY_BIND_RESET:
        return MOVE_RESET
    elif key == KEY_BIND_UNDO:
        return MOVE_UNDO
    elif not key.isdigit():
        return MOVE_ILLEGAL

    key = int(key)

    if key < 1 or key > NUMBER_OF_COLUMNS:
        return MOVE_ILLEGAL
    else:
        return key - 1


def handle_move(move, row):
    """ Update all the graphics for the given move
    """
    global _undo_available

    # Create a Circle object for the newly placed piece
    circle = Circle(Point((move + 2) * 2 * CIRCLE_RADIUS,
                          CIRCLE_Y_OFFSET - (row - 1) * 2 * CIRCLE_RADIUS), CIRCLE_RADIUS)
    _circles_list.append(circle)

    # Set its color according to the owner
    if _current_player == PLAYER:
        circle.setFill(PLAYER_COLOR)
        set_move(AI)
    else:
        circle.setFill(AI_COLOR)
        set_move(PLAYER)

    # Draw it onto the screen
    circle.draw(_window)

    _undo_available = True


def undo_move():
    """ Undo all the interface changes of the last move
    """
    global _undo_available

    if not _undo_available:
        return

    _circles_list.pop().undraw()

    if _current_player == PLAYER:
        set_move(AI)
    else:
        set_move(PLAYER)

    _undo_available = False


def get_current_player():
    """ Returns the player that currently has the move
    """
    return _current_player


def is_exiting():
    """ Returns True if we've already closed the game window, False otherwise
    """
    return _window.isClosed()


def handle_game_over(outcome):
    """ Inform the user about a game over
    """
    print outcome

    # Hide the move indicator
    _move_indicator.undraw()

    # Paint the background in victory colors
    if outcome == OUTCOME_AI:
        _window.setBackground(AI_WIN_COLOR)
    elif outcome == OUTCOME_PLAYER:
        _window.setBackground(PLAYER_WIN_COLOR)
    else:
        _window.setBackground(DRAW_COLOR)

    # Wait for the user to reset
    while _window.getKey() != KEY_BIND_RESET:
        continue

    _move_indicator.draw(_window)
    _window.setBackground(BACKGROUND_COLOR)
    reset()


def handle_illegal_move():
    """ Creates a red flash on the screen to indicate an invalid move
    """
    for i in range(0, 15):
        _window.setBackground(color_rgb(255, 18 * i, 18 * i))

    _window.setBackground(BACKGROUND_COLOR)
