from graph import Graph, Node
from board import Board
#from util import print_board, print_slide, print_swing, reformat_board, part2_to_part1, part1_to_part2
import random
import time

"""start = time.process_time()
graph = Graph("UPPER")
print(graph.simple_best_move())
print(time.process_time() - start)
"""

"""
# to record program runtime
start = time.process_time()
"""
"""
graph = Graph("UPPER")
random.seed()
def test_moves(root, depth):
    if depth > 10:
        return
    adjacents = root.generate_nodes()
    print(adjacents.shape)
    #rand_pick = random.randint(0, len(adjacents))
    test_moves(random.choice(adjacents.flatten()), depth + 1)
test_moves(graph.root, 0)
"""
"""draw_board = Board(
                    thrown_uppers = {"s": [], "p": [(0,0),(-1,1)], "r":[(-3,0), (2,-1)]},
                    thrown_lowers = {"s":[], "p":[(-4,2), (-4,4)], "r":[(0,-4)]},
                    unthrown_uppers = 0,
                    unthrown_lowers = 0,
                    turn = 30,
                    move = None
                    )

print(draw_board.is_draw(), draw_board.is_win("UPPER"), draw_board.is_win("LOWER"))

board = Board(
                    thrown_uppers = {"s": [], "p": [(0,0),(-1,1)], "r":[(-3,0), (2,-1)]},
                    thrown_lowers = {"s":[(0,2)], "p":[(-4,2), (-4,4)], "r":[(0,-4)]},
                    unthrown_uppers = 0,
                    unthrown_lowers = 0,
                    turn = 30,
                    move = None
                    )

print(board.is_draw(), board.is_win("UPPER"), board.is_win("LOWER"), board.has_invincible("LOWER"))

board = Board(
                    thrown_uppers = {"s": [], "p": [], "r":[(-3,0)]},
                    thrown_lowers = {"s":[(0,2)], "p":[(-4,2), (-4,4)], "r":[(0,-4)]},
                    unthrown_uppers = 0,
                    unthrown_lowers = 0,
                    turn = 30,
                    move = None
                    )

print(board.is_draw(), board.is_win("UPPER"), board.is_win("LOWER"), board.has_invincible("LOWER"))

board = Board(
                    thrown_uppers = {"s": [], "p": [(0,0),(-1,1)], "r":[(-3,0), (2,-1)]},
                    thrown_lowers = {"s":[], "p":[], "r":[]},
                    unthrown_uppers = 0,
                    unthrown_lowers = 1,
                    turn = 30,
                    move = None
                    )

print(board.is_draw(), board.is_win("UPPER"), board.is_win("LOWER"), board.has_invincible("LOWER"), board.can_have_invincible("LOWER"))"""

board = Board(
                    thrown_uppers = {"s": [(0,3)], "p": [(0,0),(-1,1)], "r":[(-3,0)]},
                    thrown_lowers = {"s":[(0,2), (4,-4)], "p":[(-4,2), (-4,4)], "r":[(0,-4)]},
                    unthrown_uppers = 6,
                    unthrown_lowers = 5,
                    turn = 30,
                    move = None
                )

node = Node(board, "UPPER")
print(node.eval())
graph = Graph("UPPER")
graph.root = node

start = time.process_time()
print(graph.simple_best_move())
print(time.process_time() - start)
