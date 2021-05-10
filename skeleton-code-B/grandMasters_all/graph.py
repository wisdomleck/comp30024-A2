from grandMasters_all.board import Board
from grandMasters_all.linearprograms import solve_game
import numpy as np
from itertools import product
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

    def update_root(self, root):
        self.root = root

    def SM_solver(self, state, alpha, beta):
        if state.is_terminal():
            return state.eval()

        moves = state.generate_nodes()
        O, P = self.bound(moves, alpha, beta)
        d_rows = d_cols = []
        for m in range(len(moves)):
            for n in range(len(moves[m])):
                if m not in d_rows and n not in d_cols:
                    a = get_alpha(O, P, m, n)
                    b = get_beta(O, P, m, n)
                    q = moves[m,n]

                    if a >= b:
                        v = SM_solver(q, a, a + 0.01)
                        if v <= a:
                            d_rows.append(m)
                            O = np.delete(O, m, axis = 0)
                            P = np.delete(P, m, axis = 0)

                        else:
                            d_cols.append(n)
                            O = np.delete(O, n, axis = 1)
                            P = np.delete(P, n, axis = 1)

                    else:
                        v = SM_solver(q, a, b)
                        if v <= a:
                            d_rows.append(m)
                            O = np.delete(O, m, axis = 0)
                            P = np.delete(P, m, axis = 0)
                        elif v >= b:
                            d_cols.append(n)
                            O = np.delete(O, n, axis = 1)
                            P = np.delete(P, n, axis = 1)
                        else:
                            O[m,n] = P[m,n] = v

        return solve_game(P)

        def bound(self, moves, alpha, beta):
            O = np.ones(shape = moves.shape)
            P = -O
            O = np.append(O, np.full((O.shape[0], 1), beta), axis = 1)
            P = np.append(P, np.full((1, P.shape[1]), alpha), axis = 0)
            return O, P


class Node:
    def __init__(self, board, player):
        self.player = player
        self.board = board


    def is_terminal(self):
        return self.board.is_draw() or self.board.is_win("UPPER") or self.board.is_win("LOWER")

    def generate_nodes(self):
        u_moves, l_move = self.board.generate_turns()
        moves = np.empty(shape = (len(u_move), len(l_move)))

        for m in range(len(u_move)):
            for n in range(len(l_move)):
                new_node = self.board.apply_turn(u_move[m], l_move[n])
                moves[m, n] = new_node
        if self.player == "UPPER":
            return moves
        return moves.T

    def bound(self, node):
        l_bound = -1
        u_bound = 1
        opponent = "LOWER" if self.player == "UPPER" else "UPPER"

    def lower_bound(self):
        return

    def eval(self):
        if is_win(self.player):
            return 1
        if is_win(self.opponent):
            return -1
        else:
             return 0
