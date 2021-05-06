from board import Board
from linearprograms import solve_game, get_alpha, get_beta
import numpy as np
import random

class Graph:
    """
    Contains the root node which in turns contains the current in-game board.
    """
    def __init__(self, player):
        # Game starts with no thrown tokens
        empty_start = {'s':[],'p':[], 'r':[]}
        start_board = Board(empty_start, empty_start, 9, 9, 0, None)
        self.root = Node(start_board, player)
        self.cutoff = 3

    def update_root(self, player_move, opponent_move):
        self.root = self.root.generate_node(player_move, opponent_move)

    def simple_best_move(self):
        s, v, states = self.simple_SM_solver(self.root, 0)
        choice = random.choices(range(len(s)), weights = s, k = 1)[0]
        return states[choice, 0].board.move[0]

    def simple_SM_solver(self, state, depth):

        if state.is_terminal() or depth == self.cutoff:
            return None, state.eval(), None

        sub_states = state.generate_nodes()
        payoff = np.empty(sub_states.shape)
        for m in range(sub_states.shape[0]):
            for n in range(sub_states.shape[1]):
                _, u, _ = self.simple_SM_solver(sub_states[m, n], depth + 1)
                payoff[m, n] = u
        s, v = solve_game(payoff)
        return s, v, sub_states


class Node:
    def __init__(self, board, player):
        self.player = player
        self.opponent = "LOWER" if player == "UPPER" else "UPPER"
        self.board = board


    def is_terminal(self):
        return self.board.is_draw() or self.board.is_win("UPPER") or self.board.is_win("LOWER")

    def generate_node(self, player_move, opponent_move):
        if self.player == "UPPER":
            return Node(self.board.apply_turn(player_move, opponent_move), self.player)
        else:
            return Node(self.board.apply_turn(opponent_move, player_move), self.player)

    def refine_nodes(self, u_moves, l_moves):
        u_moves = np.array(u_moves)
        l_moves = np.array(l_moves)
        u_i = np.random.choice(len(u_moves), size = int(0.2*len(u_moves)), replace = False)
        u_moves = u_moves[u_i]
        l_i = np.random.choice(len(l_moves), size = int(0.2*len(l_moves)), replace = False)
        l_moves = l_moves[l_i]

        if self.player == "UPPER":
            return u_moves, l_moves
        else:
            return l_moves, u_moves

    def generate_nodes(self):
        u_moves, l_moves = self.board.generate_turns()
        player_moves, opponent_moves = self.refine_nodes(u_moves, l_moves)
        moves = np.empty(shape = (len(player_moves), len(opponent_moves)), dtype = Node)

        for m in range(moves.shape[0]):
            for n in range(moves.shape[1]):
                moves[m, n] = self.generate_node(player_moves[m], opponent_moves[n])
        return moves

    def eval(self):
        if self.board.is_win(self.player):
            return 1
        if self.board.is_win(self.opponent):
            return -1
        if self.board.is_draw():
            return 0

        # Features: throw_diff, scissor_diff, paper_diff, rock_diff, median row
        unthrown_diff = self.board.unthrown_diff()
        dom_diff = self.board.dominance_diff()
        thrown_diff = self.board.thrown_diff()
        #print(unthrown_diff, dom_diff, thrown_diff)
        value = 0.2 * unthrown_diff + 0.25*dom_diff + 0.1*thrown_diff
        capped_val = min(max(value, -1), 1)

        if self.player == "UPPER":
            return capped_val
        else:
            return -capped_val
