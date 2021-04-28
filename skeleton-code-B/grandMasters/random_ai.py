import random

class RandomAI:
    def __init__(self, player):
        self.us = player

        if player == "UPPER":
            self.opponent = "LOWER"
        else:
            self.opponent = "UPPER"

    def choose_next_move(self, board):
        upper, lower = board.generate_turns()
        if self.us == "UPPER":
            return random.choice(upper)
        return random.choice(lower)
