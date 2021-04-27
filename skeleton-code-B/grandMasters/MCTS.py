
from board import Board
import random

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
        self.last_action = last_action
        self.children = []

        # Dictionary to keep track of wins (1), losses (-1), draws (0)
        self.results = {}
        self.results[1] = 0
        self.results[0] = 0
        self.results[-1] = 0

        self.num_simulations = 0


        # In the current board, who's move is it?
        self.player = player

        # Dict?
        self.moves_to_consider = self.get_possible_moves()


    """ Get possible moves from current state """
    def get_possible_moves(self):
        movesdict = self.board.generate_seq_turn()[self.player]
        moves = []

        for key in movesdict.keys():
            moves += movesdict[key]
        # Moves is a list with all possible moves
        return moves

    """ Given a root node, generate children to explore """
    def expand(self):
        move = self.moves_to_consider.pop()
        nextboard = self.board.apply_turn(move)

        child = MCTSNode(nextboard, move, self.switch_player())

        self.children.append(child)

        return

    """ Chooses a random move from a player's moveset. Used for rollout in MCTS.
        Must pass in the correct player's dictionary of moves
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
            rand_movetype = 0
        else:
            rand_movetype = random.randint(0, len(possible_moves)-1)


        # Retrieve a random index to a move in the dictionary
        if len(moves[possible_moves[rand_movetype]]) - 1 == 0:
            rand_move = 0
        else:
            rand_move = random.randint(0, len(moves[possible_moves[rand_movetype]]) - 1)

        # Index the move in the dict
        return moves[possible_moves[rand_movetype]][rand_move]

    """ After a move is made, pass in the next player's turn into child nodes """
    def switch_player(self):
        if self.player == "UPPER":
            return "LOWER"
        else:
            return "UPPER"

    """ Simulates a random game from given board
        For each iteration, move both player's pieces simultaneously
    """
    def rollout(self):
        current_board = self.board

        while not current_board.is_terminal():
            rand_move_p1 = self.choose_random_move(current_board.generate_seq_turn()[self.player])
            rand_move_p2 = self.choose_random_move(current_board.generate_seq_turn()[self.switch_player()])

            if self.player == "UPPER":
                current_board = current_board.apply_turn(rand_move_p1, rand_move_p2)
            else:
                current_board = current_board.apply_turn(rand_move_p2, rand_move_p1)
            current_board.turn += 1
            #print(current_board)
        return current_board.game_result(), current_board.turn
