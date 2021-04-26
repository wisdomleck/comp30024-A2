
from board import Board

MOVETYPES = ["THROW", "SLIDE", "SWING"]

""" UCB1 formula for node selection in the MCTS algorithm """
def ucb1_formula(value, games, c, N, ni):
    return value/games + c*sqrt(log(N)/ni)


""" Class to represent a node in the MCTS "statistics tree" """
class MCTSNode:
    """ Initialises a node in the MCTS tree, keeps track of relevant
    statistics used in the algorithm """
    def __init__ (self, board, parent = None, last_action = None, player):
        self.board = board
        self.parent = parent
        self.last_action = last_action
        self.adjacent_nodes = []
        self.utility_value = 0
        self.num_simulations = 0

        # Dict?
        self.moves_to_consider = self.get_possible_moves()

        self.player = player

    """ Get possible moves from current state """
    def get_possible_moves(self):
        moves = self.board.generate_seq_turn()[self.player]
        # Moves is a dict with movetype: moves
        return moves

    """ Given a root node, generate children to explore """
    def expand(self):
        possible_moves = self.board.generate_seq_turn()
        nextboard = self.board.apply_turn(rand_move)

    def choose_random_move(self, moves):
        rand_movetype = random.randint(0, 3)
        rand_move = random.randint(0, len(moves[MOVETYPES[rand_movetype]]))
        return rand_move

    """ After a move is made, pass in the next player's turn into child nodes """
    def switch_player(self):
        if player == "UPPER":
            return "LOWER"
        else:
            return "UPPER"
