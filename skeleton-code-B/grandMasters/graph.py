from board import Board
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

    def SM_solver(self, root):
        if root.board.winstate():
            return root.board.eval()
        if self.player == "UPPER":
            player_moves, opponent_moves = root.board.generate_turns()
        else:
            opponent_moves, player_moves = root.board.generate_turns()


        for p_move in player_moves:
            for o_move in opponent_moves:
                self.SM_solver(self.root)


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
    def new_node(self, player_move, opponent_move):
