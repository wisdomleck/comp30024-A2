
from board import Board
import random
from util import print_board, print_slide, print_swing, reformat_board, part2_to_part1, part1_to_part2
from collections import defaultdict
import numpy as np

MOVETYPES = ["THROWS", "SLIDES", "SWINGS"]

""" UCB1 formula for node selection in the MCTS algorithm """
def ucb1_formula(value, games, c, N, ni):
    return value/games + c*sqrt(log(N)/ni)


""" Class to represent a node in the MCTS "statistics tree" """
class MCTSNode:
    """ Initialises a node in the MCTS tree, keeps track of relevant
    statistics used in the algorithm """
    def __init__ (self, board, player, parent = None, last_action = None):
        self.board = board
        self.parent = parent

        # Move in form of (upper, lower) to get to current board
        self.last_action = last_action
        self.children = []

        # Dictionary to keep track values for each possible move for upper/lower
        # Used for DUCT algorithm for simultaneous MCTS
        self.resultsUpper = defaultdict(lambda: 0)
        self.resultsLower = defaultdict(lambda: 0)

        self.num_visits = 0
        # In the current board, who's move is it?
        self.player = player

        # Possible moves for upper and lower
        self.simultaneous_moves = self.get_possible_moves()

    """ Get possible moves from current state """
    def get_possible_moves(self):
        upper, lower = self.board.generate_turns()
        moveslist = []
        for uppermove in upper:
            for lowermove in lower:
                moveslist.append((uppermove, lowermove))
        # Moves is a list with all possible moves
        return moveslist

    """ Given a root node, generate children to explore """
    def expand(self):
        move = self.simultaneous_moves.pop()

        nextboard = self.board.apply_turn2(move[0], move[1])

        child = MCTSNode(nextboard, self.switch_player(), parent=self, last_action=move)

        self.children.append(child)

        return child

    """ returns whether the game is done or not """
    def is_terminal_node(self):
        return self.board.is_win("UPPER") or self.board.is_win("LOWER") or self.board.is_draw()

    """ Chooses a random move from a player's moveset. Used for rollout in MCTS.
        Must pass in the correct player's dictionary of moves
        EDIT THIS: USE RANDOM.CHOICE instead of doing random indexes
    """
    def choose_random_move(self, moves):
        # Need to determine whether these type of moves are possible, i.e if there are any moves of that type
        possible_moves = ["THROWS", "SLIDES", "SWINGS"]

        # Get rid of movetypes with no moves
        for i in range(2, -1, -1):
            if not moves[possible_moves[i]]:
                possible_moves.pop(i)

        # Throw, slide or swing
        if len(possible_moves) == 1:
            rand_movetype = possible_moves[0]
        else:
            rand_movetype = random.choice(possible_moves)


        # Retrieve a random index to a move in the dictionary
        if len(moves[rand_movetype]) - 1 == 0:
            rand_move = moves[rand_movetype][0]
        else:
            rand_move = random.choice(moves[rand_movetype])

        # Index the move in the dict
        return moves[rand_movetype][rand_move]

    """ After a move is made, pass in the next player's turn into child nodes """
    def switch_player(self):
        if self.player == "UPPER":
            return "LOWER"
        else:
            return "UPPER"

    """ Simulates a random game from given board
        For each iteration, move both player's pieces simultaneously
    """
    def rollout_random(self):
        current_board = self.board
        #print("NEW GAME")
        while not (current_board.is_win("UPPER") or current_board.is_draw() or current_board.is_win("LOWER")):
            # Do this in order to randomize between movetype, then randomise between move
            #rand_move_p1 = self.choose_random_move(current_board.generate_seq_turn()[self.player])
            #rand_move_p2 = self.choose_random_move(current_board.generate_seq_turn()[self.switch_player()])

            # Do this for just random moves altogether
            # CHOOSE NEXT MOVE TO APPLY IN ROLLOUT
            upper, lower = current_board.generate_turns()
            rand_move_p1 = random.choice(upper)
            rand_move_p2 = random.choice(lower)

            current_board = current_board.apply_turn2(rand_move_p1, rand_move_p2)

            #print(current_board)
            #print_board(part2_to_part1(current_board))
            #print(current_board)
            #print(part1_to_part2(part2_to_part1(current_board)))
        return current_board.game_result(), current_board.turn

    """ Randomly chooses a greedy move """
    def rollout_greedy(self):
        current_board = self.board
        #print("NEW GAME")
        while not (current_board.is_win("UPPER") or current_board.is_draw() or current_board.is_win("LOWER")):

            # Determine greedy moves then choose random move
            upper = current_board.determine_greedy_moves("UPPER")
            lower = current_board.determine_greedy_moves("LOWER")

            """
            print("TURN:", current_board.turn)
            print("UPPER:", upper)
            print("LOWER:", lower)
            print("upper_thrown:", current_board.thrown_uppers)
            print("lower_thrown:", current_board.thrown_lowers)"""
            rand_move_p1 = random.choice(upper)
            rand_move_p2 = random.choice(lower)

            current_board = current_board.apply_turn2(rand_move_p1, rand_move_p2)


        return current_board.game_result(), current_board.turn

    # Back propagates the result using DUCT. Update results in decoupled way
    # and add results for the move
    # Last action for root node is none
    def backpropagate(self, result):
        self.num_visits += 1
        #print(self.last_action)
        #print(self.board.thrown_uppers)
        #print(self.board.thrown_lowers)

        if self.parent is not None:
            # DOBULE CHECK THIS PARENT PROPAGATE CALL
            self.parent.resultsUpper[self.last_action[0]] += result
            self.parent.resultsLower[self.last_action[1]] += -result
        if self.parent is not None:
            self.parent.backpropagate(result)

    # Stop expanding if no more upper moves or no more lower moves
    def is_fully_expanded(self):
        return len(self.simultaneous_moves) == 0

    def best_child(self, c_param = 0.1):
        choices_weights_upper = [(c.q_upper() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        choices_weights_lower = [(c.q_lower() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        #print(choices_weights_upper)
        #print(self.children)
        upper_move = self.children[np.argmax(choices_weights_upper)].last_action[0]
        lower_move = self.children[np.argmax(choices_weights_upper)].last_action[1]

        # Assume that a node made from upper_move, lower_move exists?
        for child in self.children:
            if (upper_move, lower_move) == child.last_action:
                return child

        return None

    # Function that selects a node to rollout.
    def tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def q_upper(self):
        utility_value_upper = self.resultsUpper[self.last_action[0]]
        return utility_value_upper

    def q_lower(self):
        utility_lower = self.resultsLower[self.last_action[1]]
        return utility_lower

    def n(self):
        return self.num_visits

    def best_action(self):
        simulation_no = 1000

        for i in range(simulation_no):

            v = self.tree_policy()
            # Because rollout is giving out a tuple rn
            reward = v.rollout_random()[0]

            # Need to do: update current node -> backpropagate starting from parent since we're using last_action and root has no last_action
            if self.last_action:
                v.resultsUpper[self.last_action[0]] += result
                v.resultsLower[self.last_action[1]] += -result
            v.backpropagate(reward)

        return self.best_child(c_param=0.05)
