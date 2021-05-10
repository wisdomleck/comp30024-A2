import random

class RandomAI:
    def __init__(self, player):

        if player == "UPPER":
            self.us = "UPPER"
            self.opponent = "LOWER"
        else:
            self.us = "LOWER"
            self.opponent = "UPPER"

    def choose_next_move(self, board):
        upper, lower = board.generate_turns()
        if self.us == "UPPER":
            #print(upper)
            return random.choice(upper)
        #print(lower)
        return random.choice(lower)
