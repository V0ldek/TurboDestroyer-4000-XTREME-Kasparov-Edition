#####
# This module contains all the logic for AI behaviour
#####

import random
import math
import time
from connectfour.GameplayStatics import *

# Alpha-beta search


class Vertex:
    """ Class for a game tree vertex, used in alpha_beta search
    """

    def __init__(self, prev_value, num, board, move):
        # The estimated value of the node based on evaluation function or previous searches
        self.prev_value = prev_value

        # The number of the vertex
        self.num = num

        # The board associated with this vertex
        self.board = board

        # The move that was performed to get to this vertex
        self.move = move

        # How far from the deepest end-node are we
        self.max_moves = 0

        # Was this vertex expanded and its child moves generated
        self.expanded = False


# The game tree
G = []

# Killer heuristic
killer = []

# Transposition table
transposition_table = {}


class tt_entry:
    """A plain data type for transposition table entry"""

    def __init__(self, entry_type, value, depth, max_moves):
        # Type of the entry - 'exact', 'upper', 'lower'
        self.type = entry_type

        # Values associated with the entry
        self.value = value
        self.max_moves = max_moves

        # Depth of the entry vertex
        self.depth = depth


def add_entry(h, alpha, beta, value, depth, max_moves):
    """Produce and add an entry with the given hash to the transposition table"""
    entry = tt_entry('exact', value, depth, max_moves)

    if value <= alpha:
        tt_entry.type = 'lower'
    elif value >= beta:
        tt_entry.type = 'upper'

    transposition_table[h] = entry


def alpha_beta_order_moves(children, depth, player):
    """Order the moves in the best possible way - killer move first, rest sorted by values of previous searches"""
    without_killer = []
    new_children = []

    for child in children:
        if child.move != killer[depth]:
            without_killer.append(child)
        else:
            new_children.append(child)

    if player == PLAYER:
        without_killer.sort(key=lambda vertex: -vertex.prev_value)
    else:
        without_killer.sort(key=lambda vertex: vertex.prev_value)

    for child in without_killer:
        new_children.append(child)

    return new_children


def alpha_beta(v, depth, alpha, beta, player, evaluate, start_clock):
    """ Recursive alpha-beta algorithm that terminates after a set time has passed since the start_clock
    """

    # If we have used all available time, terminate the search
    if (time.clock() - start_clock) * 1000 >= TIME_TO_MOVE:
        return 0

    # Get the entry for current board, determine if we can use it
    h = v.board.hash
    entry = transposition_table.get(h)

    if entry is not None and entry.depth >= depth:
        if entry.type == 'exact':
            v.prev_value = entry.value
            v.max_moves = entry.max_moves

            return entry.value
        elif entry.type == 'upper':
            beta = min(entry.value, beta)
        else:
            alpha = max(entry.value, alpha)

        if beta <= alpha:
            v.prev_value = entry.value
            v.max_moves = entry.max_moves

            return entry.value

    # Copy the original alpha-beta values
    original_alpha = alpha
    original_beta = beta

    # If we have reached the desired tree depth, return static evaluation value of this node
    if depth == 0:
        value = evaluate(v.board)

        v.prev_value = value

        add_entry(h, original_alpha, original_beta, value, depth, v.max_moves)

        return value

    # If this node is an end-node, assign a static evaluation value to it and make sure we will never visit it again
    if not v.expanded and v.board.check_game_over() != OUTCOME_NOTHING:
        value = evaluate(v.board)

        v.prev_value = value
        v.expanded = True

        add_entry(h, original_alpha, original_beta, value, depth, v.max_moves)

        return value

    # If this node has been expanded, so its children have prev_values assigned, sort them in the optimal order
    # If the node has not been expanded yet, generate its child moves
    if v.expanded:
        G[v.num] = alpha_beta_order_moves(G[v.num], depth, player)
    else:
        for x in range(NUMBER_OF_COLUMNS):
            if v.board.is_move_legal(x):
                new_v = Vertex(0, len(G), v.board.make_move(x, player), x)
                G.append([])
                G[v.num].append(new_v)

        v.expanded = True

    # If we are the maximising player
    if player == PLAYER:
        value = -INF

        # For each child recurse down the tree and update our alpha and current values
        for child in G[v.num]:
            new_value = alpha_beta(child, depth - 1, alpha, beta, AI, evaluate, start_clock)

            if new_value > value:
                value = new_value
                v.max_moves = child.max_moves + 1
            elif new_value == value:
                v.max_moves = max(v.max_moves, child.max_moves + 1)

            alpha = max(alpha, value)

            # Alpha cutoff
            if beta <= alpha:
                v.prev_value = value

                # A move that caused a cutoff becomes the new killer move
                killer[depth] = child.move

                add_entry(h, original_alpha, original_beta, value, depth, v.max_moves)

                return value
    # If we are the minimising player
    else:
        value = INF

        # For each child recurse down the tree and update our beta and current values
        for child in G[v.num]:
            new_value = alpha_beta(child, depth - 1, alpha, beta, PLAYER, evaluate, start_clock)

            if new_value < value:
                value = new_value
                v.max_moves = child.max_moves + 1
            elif new_value == value:
                v.max_moves = max(v.max_moves, child.max_moves + 1)

            beta = min(beta, value)
            v.max_moves = max(v.max_moves, child.max_moves + 1)

            # Beta cutoff
            if beta <= alpha:
                v.prev_value = value

                # A move that caused a cutoff becomes the new killer move
                killer[depth] = child.move

                add_entry(h, original_alpha, original_beta, value, depth, v.max_moves)

                return value

    v.prev_value = value

    add_entry(h, original_alpha, original_beta, value, depth, v.max_moves)

    return value


def make_alpha_beta_move(board, evaluate, player, depth=NUMBER_OF_COLUMNS * NUMBER_OF_ROWS):
    """ Performs alpha-beta search to find the best possible move using the given evaluate function
    """
    global G, killer, transposition_table

    # Clear the game tree
    G = []
    transposition_table = {}

    # Create a root
    root = Vertex(0, 0, board, 0)
    G.append([])

    # Make sure we always look through the next moves we can take
    if transposition_table.get(root.board.hash) is not None:
        transposition_table[root.board.hash] = None

    # Set up the timer
    t = time.clock()

    best = None

    # Iterative deepening
    for d in range(depth):

        # If we have exceeded our time, terminate
        if (time.clock() - t) * 1000 >= TIME_TO_MOVE:
            break

        # Reset the killer heuristic table
        killer = [-1 for x in range(NUMBER_OF_COLUMNS * NUMBER_OF_ROWS + 1)]

        # Perform a full alpha-beta pass until we reach the desired depth, all nodes are explored or time runs out
        alpha_beta(root, d + 1, -2 * INF, 2 * INF, player, evaluate, t)

        # If we terminated the d-depth search early, there is no use to update our best move, so terminate
        if (time.clock() - t) * 1000 >= TIME_TO_MOVE:
            break

        best = None

        if DEBUG:
            print "for depth " + str(d + 1) + " value = " + str(root.prev_value)

        # If we are the maximising player, find the move with the highest min-max value
        # Among moves with equal values choose the one that has more moves until the end of the game
        if player == PLAYER:
            value = -2 * INF

            for child in G[root.num]:
                if child.prev_value > value or (child.prev_value == value and child.max_moves > best.max_moves):
                    value = child.prev_value
                    best = child

                    if value == INF:
                        return best.move
        # If we are the minimising player, find the move with the lowest min-max value
        # Among moves with equal values choose the one that has more moves until the end of the game
        else:
            value = 2 * INF

            for child in G[root.num]:
                if child.prev_value < value or (child.prev_value == value and child.max_moves > best.max_moves):
                    value = child.prev_value
                    best = child

                    if value == -INF:
                        return best.move

    if DEBUG:
        print "move found in " + str((time.clock() - t) * 1000)

    return best.move


def basic_evaluate(board):
    """ Basic evaluation function. Prioritises:
    1) Win the game, if able
    2) Don't lose the game
    3) Places that are nearest to the middle of the point + a bit of randomisation
    """
    value = 0

    # Check if the game is won after this move
    game_over = board.check_game_over()

    if game_over == OUTCOME_PLAYER:
        return INF
    elif game_over == OUTCOME_AI:
        return -INF

    # Evaluate the board based on the position of all pieces relative to the board's centre
    for y in range(NUMBER_OF_ROWS):
        for x in range(NUMBER_OF_COLUMNS):
            place_score = 1 + NUMBER_OF_COLUMNS + NUMBER_OF_ROWS \
                          - abs(NUMBER_OF_ROWS / 2 - y) - abs(NUMBER_OF_COLUMNS / 2 - x)

            if y == 0 and x == 3:
                place_score += 10

            # A bit of randomness can prove you no wrong
            place_score += random.randint(0, 1)

            if board.get_piece(y, x) == PLAYER:
                value += place_score
            elif board.get_piece(y, x) == AI:
                value -= place_score

    return value


def make_random_move():
    """ Returns a random, not necessarily valid move on the current board
    """
    return random.randint(0, NUMBER_OF_COLUMNS - 1)


def make_evaluated_move(board, evaluate, player):
    """ Returns the best move according to the evaluate function
    """
    maxx = -10 * INF
    best_move = 0

    for x in range(NUMBER_OF_COLUMNS):
        if board.is_move_legal(x):
            evaluation = evaluate(board.make_move(x, player), player)

            if evaluation > maxx:
                maxx = evaluation
                best_move = x

    if DEBUG:
        print "the best move is " + str(best_move) + " of value " + str(maxx)
    
    return best_move


def reset():
    """Reset all the AI arrays"""
    global G, transposition_table, killer

    G = []
    transposition_table = {}
    killer = []
