#####
# Contains a class representing the game board inside computer's memory and functions that manipulate it
#####

import random
from connectfour.GameplayStatics import *

# Zobrist hashing random bits


def gen_random_bits(n):
    """Generates a random n-bit number"""
    pot = 1
    l = 0

    for i in range(n):
        l += pot * random.randint(0, 1)
        pot *= 2

    return l


# Table containing Zobrist hash values for each cell
hash_table = []

# Initialise the hash_table with random bits
for cell in range(NUMBER_OF_ROWS * NUMBER_OF_COLUMNS):

    hash_table.append([])

    hash_table[cell].append(gen_random_bits(64))
    hash_table[cell].append(gen_random_bits(64))


class Board:
    """ The class representing the game board, contains functions to manipulate the board
    It is immutable by design, so once created it cannot be changed This is why making a move returns a new Board object
    An empty place is represented by a ' ' char, Player's piece is represented by an 'O' char
    and AI piece is represented by an 'X' char
    """

    def __init__(self):
        """ Creates an empty board and the counters list
        """
        # List of lists representing the game board with chars ' ', 'O' and 'X'
        self._board = [[' ' for x in range(NUMBER_OF_COLUMNS)] for y in range(NUMBER_OF_ROWS)]

        # List counting the amount of pieces in each column, to speed up move generation
        self._counters = [0 for x in range(NUMBER_OF_COLUMNS)]

        # The last move that was performed on the board
        self.last_move = -1

        # The Zobrist hash of the board
        self.hash = 0

    def copy(self):
        """ Returns a new object exactly the same as this one
        """
        new = Board()

        new._board = [[self._board[y][x] for x in range(NUMBER_OF_COLUMNS)] for y in range(NUMBER_OF_ROWS)]
        new._counters = [self._counters[x] for x in range(NUMBER_OF_COLUMNS)]
        new.hash = self.hash

        return new

    def print_board(self, f):
        """ Prints the board to standard output
        """
        for y in range(NUMBER_OF_ROWS - 1, -1, -1):
            f.write(str(self._board[y]) + "\n")
        f.write("\n\n")

    def is_move_legal(self, column):
        """ Returns True if a legal move can be made in the given column, False otherwise
        """
        if self._counters[column] >= NUMBER_OF_ROWS:
            return False
        else:
            return True

    def get_piece(self, row, column):
        """ Returns the player that put a piece on the given place
        """
        return self._board[row][column]

    def get_counter(self, column):
        """ Returns the amount of pieces currently in the given column
        """
        return self._counters[column]

    def make_move(self, column, player):
        """ Returns a new Board() object with an appropriate char on top of the given column
        ('O' if is_player equals True, 'X' if it equals False)
        If the column is already full an IndexError exception is raised
        """
        row = self._counters[column]

        # Create a new Board() object, since Board is immutable
        new = self.copy()

        try:
            if player == PLAYER:
                new._board[row][column] = PLAYER
            else:
                new._board[row][column] = AI
        except IndexError:
            print "Board.make_move(" + str(column) + ", " + player + "tried to make an illegal move"

        # Update the appropriate counter
        new._counters[column] = row + 1

        # Set the last move to the one just performed
        new.last_move = column

        # Update the hash of the board accordingly
        cell_num = row * NUMBER_OF_COLUMNS + column

        if player == PLAYER:
            new.hash ^= hash_table[cell_num][0]
        else:
            new.hash ^= hash_table[cell_num][1]

        return new

    def check_game_over(self):
        """ Checks the game ending conditions and returns a string representing the outcome
        'Player' if Player won, 'AI' if AI won, 'Draw' if the game ended in a draw or 'Null' if the game is not over
        """

        # If the board is full, we have a draw
        if self._counters.count(NUMBER_OF_ROWS) == NUMBER_OF_COLUMNS:
            return OUTCOME_DRAW

        # Utility function
        def check_line(x, y, x_step, y_step):
            """ Checks a straight line from point (x, y) with step (x_step, y_step) for any 4 connected pieces
            """
            cnt = 0
            prev = ' '

            while 0 <= x < NUMBER_OF_COLUMNS and 0 <= y < NUMBER_OF_ROWS:
                if self._board[y][x] == prev:
                    cnt += 1

                    if cnt == NUMBER_TO_CONNECT:
                        if prev == PLAYER:
                            return OUTCOME_PLAYER
                        elif prev == AI:
                            return OUTCOME_AI
                else:
                    prev = self._board[y][x]
                    cnt = 1

                x += x_step
                y += y_step

            return OUTCOME_NOTHING

        last_x = self.last_move
        last_y = self._counters[self.last_move] - 1

        # Check the straight, vertical line through the (last_x, last_y) point
        outcome = check_line(last_x, 0, 0, 1)

        if outcome != OUTCOME_NOTHING:
            return outcome

        # Check the straight, horizontal line through the (last_x, last_y) point
        outcome = check_line(0, last_y, 1, 0)

        if outcome != OUTCOME_NOTHING:
            return outcome

        minn = min(last_x, last_y)

        # Check the straight, diagonal line through the (last_x, last_y) point, going from bottom-left to top-right
        outcome = check_line(last_x - minn, last_y - minn, 1, 1)

        if outcome != OUTCOME_NOTHING:
            return outcome

        minn = min(NUMBER_OF_COLUMNS - last_x - 1, last_y)

        # Check the straight, diagonal line through the (last_x, last_y) point, going from bottom-right to top-left
        outcome = check_line(last_x + minn, last_y - minn, -1, 1)

        return outcome
