#####
# This file contains the gameplay crucial constants to be used throughout the program
#####

# Dimensions of the game board
NUMBER_OF_ROWS = 6
NUMBER_OF_COLUMNS = 7

# The amount of pieces one needs to connect in order to win
NUMBER_TO_CONNECT = 4

# Aliases for players
AI = 'X'
PLAYER = 'O'

# Aliases for victory check outcomes
OUTCOME_NOTHING = 'null'
OUTCOME_AI = 'ai'
OUTCOME_PLAYER = 'player'
OUTCOME_DRAW = 'draw'

# Aliases for different kinds of moves
MOVE_ILLEGAL = 'illegal'
MOVE_RESET = 'reset'
MOVE_UNDO = 'undo'

# Infinity value
INF = 1000000000

# Time for one move (in milliseconds)
TIME_TO_MOVE = 10000
