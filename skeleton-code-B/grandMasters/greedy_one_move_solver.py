
""" Function that given a board state, chooses the next "best" move. If there
are multiple, then chooses one of these best moves randomly.
"""

class SillyMoveChooserAI:
    def __init__(self, player):
        self.player = player
        
    def choose_next_move(board):
        """ For now, play a set opening in order to gain space """
        if board.turn == 0:
            return ("THROW", "r", (-4, 0))
        if board.turn == 1:
            return ("THROW", "s", (-3, 4))
        if board.turn == 2:
            return ("THROW", "p", (-2, 2))
        if board.turn == 3:
            return ("THROW", "r", (-1, 4))
        if board.turn == 4:
            return ("THROW", "s", (0, -1))

        capture_moves = []
        escape_moves = []
        dist_closing_moves = []

        possible_moves = board.get_possible_moves()
