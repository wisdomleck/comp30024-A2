from graph import Graph
from board import Board
from MCTS import MCTSNode
from util import print_board, print_slide, print_swing, reformat_board, part2_to_part1, part1_to_part2
import random
from greedy_one_move_solver import SillyMoveChooserAI
import time

"""# to record program runtime
start = time.process_time()

random.seed()
def test_moves(root, depth):
    if depth > 10:
        return
    print(root.board)
    adjacents = root.adjacent_nodes()
    #rand_pick = random.randint(0, len(adjacents))
    test_moves(random.choice(adjacents), depth + 1)"""



draw_board = Board(
                    thrown_uppers = {"s": [], "p": [(0,0),(-1,1)], "r":[(-3,0), (2,-1)]}
                    thrown_lowers = {"s":[], "p":[(-4,2), (-4,4)], "r":[(0,-4)]}
                    unthrown_uppers = 0
                    unthrown_lowers = 0
                    turn = 30
                    move = None
                    )

print(draw_board.is_draw())
