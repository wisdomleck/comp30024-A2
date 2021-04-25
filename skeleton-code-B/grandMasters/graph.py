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
            adjacents.append(Node(self.board.apply_turn(u_move, l_move)))
        return adjacents
