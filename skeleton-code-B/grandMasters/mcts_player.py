from grandMasters.graph import Graph
from grandMasters.board import Board
from grandMasters.greedy_one_move_solver import SillyMoveChooserAI
from grandMasters.MCTS import MCTSNode

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
        self.ai = MCTSNode(self.own_board, self.us, None, None)

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """

        # book learnt moves
        if self.own_board.turn <= 4:
            return self.opening(self.us, self.own_board.turn)
        # put your code here
        num_sims = len(self.ai.simultaneous_moves)*5
        if self.us == "UPPER":
            node = self.ai.best_action(num_sims)
            return node.last_action[0]
        else:
            node = self.ai.best_action(num_sims)
            return node.last_action[1]
        return move

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
            self.ai = MCTSNode(self.own_board, self.us, None, None)
        else:
            self.own_board = self.own_board.apply_turn2(opponent_action, player_action)
            self.ai = MCTSNode(self.own_board, self.us, None, None)
        #print("AFTER UPDATE:")
        #print(self.own_board)
        # put your code here

    """ opening moves hardcoded """
    def opening(self, player, turn):
        if player == "UPPER":
            if turn == 0:
                return ("THROW", "s", (4, -2))
            elif turn == 1:
                return ("THROW", "r", (3,-2))
            elif turn == 2:
                return ("THROW", "p", (2, -1))
            elif turn == 3:
                return ("THROW", "s", (1, 0))
            elif turn == 4:
                return ("THROW", "r", (0, 1))

        elif player == "LOWER":
            if turn == 0:
                return ("THROW", "r", (-4, 0))
            if turn == 1:
                return ("THROW", "s", (-3, 4))
            if turn == 2:
                return ("THROW", "p", (-2, 2))
            if turn == 3:
                return ("THROW", "r", (-1, 4))
            if turn == 4:
                return ("THROW", "s", (0, -1))
