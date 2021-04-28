from board import Board
from linearprograms import solve_game, get_alpha, get_beta
import numpy as np
class Graph:
    """
    Contains the root node which in turns contains the current in-game board.
    """
    def __init__(self, player):
        self.player = player
        # Game starts with no thrown tokens
        empty_start = {'s':[],'p':[], 'r':[]}
        start_board = Board(empty_start, empty_start, 9, 9, 0, None)
        self.root = Node(start_board)

    def update_root(self, root):
        self.root = root

    def SM_solver(self, state):
        if state.is_terminal():
            if state.board.is_win(self.player):
                return 1
            elif state.board.is_draw():
                return 0
            else:
                return -1

        if self.player == "UPPER":
            player_moves, opponent_moves = state.board.generate_turns()
        else:
            opponent_moves, player_moves = state.board.generate_turns()

        sim_matrix = []
        for m in player_moves:
            sim_row = []
            for n in opponent_moves:
                new_node = self.state.generate_node(self.player, m, n)
                sim_row.append(SM_solver, new_node)
        return solve_game(sim_matrix)[1]


class Node:
    def __init__(self, board):
        self.board = board

    def adjacent_nodes(self):
        """
        Generate adjacent nodes to the current nodes, where a node is adjacent
        if its board is reachable with a single move from the current node's board.
        """
        adjacents = []
        for u_move, l_move in self.board.generate_turns():
            new_board = self.board.apply_turn(u_move, l_move)
            adjacents.append(Node(new_board))
        return adjacents

    def is_terminal(self):
        return self.board.is_draw() or self.board.is_win("UPPER") or self.board.is_win("LOWER")

    def generate_node(self, player, p, o):
        if player == "UPPER":
            return Node(self.board.apply_turn(p, o))
        else:
            return Node(self.board.apply_turn(o, p))
