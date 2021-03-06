from grandMasters.graph import Graph
from grandMasters.board import Board
from grandMasters.greedy_one_move_solver import SillyMoveChooserAI

class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        if player == "upper":
            self.us = "UPPER"
            self.opponent = "LOWER"
        else:
            self.us = "LOWER"
            self.opponent = "UPPER"

        empty_start = {'s':[],'p':[], 'r':[]}
        self.own_board = Board(empty_start, empty_start, 9, 9, 0, None)
        self.ai = SillyMoveChooserAI(self.us)

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        return self.ai.choose_next_move(self.own_board)

    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        if self.us == "UPPER":
            self.own_board = self.own_board.apply_turn2(player_action, opponent_action)
        else:
            self.own_board = self.own_board.apply_turn2(opponent_action, player_action)
        print("AFTER UPDATE:")
        print(self.own_board)
        # put your code here
