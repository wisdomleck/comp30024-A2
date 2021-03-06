from graph import Graph
from board import Board
from MCTS import MCTSNode
from util import print_board, print_slide, print_swing, reformat_board, part2_to_part1, part1_to_part2
import random
from greedy_one_move_solver import SillyMoveChooserAI
import time
from evaluation import evaluate_move

# to record program runtime
start = time.process_time()
"""
random.seed()
def test_moves(root, depth):
    if depth > 10:
        return
    print(root.board)
    adjacents = root.adjacent_nodes()
    #rand_pick = random.randint(0, len(adjacents))
    test_moves(random.choice(adjacents), depth + 1)"""


"""
draw_board = Board(
                    thrown_uppers = {"s": [], "p": [(0,0),(-1,1)], "r":[(-3,0), (2,-1)]}
                    thrown_lowers = {"s":[], "p":[(-4,2), (-4,4)], "r":[(0,-4)]}
                    unthrown_uppers = 0
                    unthrown_lowers = 0
                    turn = 30
                    move = None
                    )

testboard = testboard.apply_turn2((("THROW"), "r", (3,-2)), ("THROW", "r", (3,-2)))
testboard = testboard.apply_turn2((("THROW"), "s", (-1, 1)), ("THROW", "p", (3,-2)))

print(testboard)
"""
# MCTS TESTING HERE ----------------------------------------------------------------------------------------

"""
graph = Graph("UPPERS")

board = graph.root.board

print(board)
print_board(part2_to_part1(board))
print(part1_to_part2(part2_to_part1(board)))

mctsnode = MCTSNode(board, "UPPER")
print(len(mctsnode.get_possible_moves()))
upper_wins = 0
lower_wins = 0
ties = 0
total_turns = 0

total_value = 0


for i in range(10):
    result, turns = mctsnode.rollout_random()
    if result == 1:
        upper_wins += 1
    elif result == -1:
        lower_wins += 1
    else:
        ties += 1
    total_turns += turns
    total_value += result
print(f"UpperWins: {upper_wins}\nLowerWins: {lower_wins}\nTies: {ties}\nAvgTurnsNeeded: {total_turns/1000}")
print(total_value)
"""
"""
randomboard = mctsnode.generate_random_board(30)

print("RANDOM BOARD")
print_board(part2_to_part1(randomboard))

randomuppers = randomboard.thrown_uppers
randomlowers = randomboard.thrown_lowers
randomturn = randomboard.turn

print(randomuppers)
print(randomlowers)
"""
"""
u = {'s': [(-4, -2), (2, 4)], 'p': [], 'r': []}
l = {'s': [], 'p': [], 'r': [(0, 3)]}
testboard = Board(u, l, 0, 0, 37, None)
print_board(part2_to_part1(testboard))
print(testboard.generate_turns()[0])
"""

thrown_uppers = {'s': [], 'p': [(4,-1), (3,-3), (0,-3)], 'r': [(4,-3)]}
thrown_lowers = {'s': [(0,-1), (-3,4), (-4,3)], 'p': [(-2,2)], 'r': [(-4,0), (-1,4)]}

testboard = Board(thrown_uppers, thrown_lowers, 1, 1, 0, None)
print_board(part2_to_part1(testboard))

mctsnode = MCTSNode(testboard, "UPPER")
print(len(mctsnode.simultaneous_moves))
selectednode = mctsnode.best_action(len(mctsnode.simultaneous_moves) * 50)
print("MCTS BEST MOVE:", selectednode.last_action)
upper, lower = testboard.generate_turns()

maxupper = -100000
maxlower = -100000

for uppermove in upper:
    eval = evaluate_move(testboard, uppermove, "UPPER")
    print("UPPER EVALS")
    print(eval)
    if eval > maxupper:
        maxupper = eval
        bestuppermove = uppermove

for lowermove in lower:
    eval = -1*evaluate_move(testboard, lowermove, "LOWER")
    print("LOWER EVALS")
    print(eval)
    if eval > maxlower:
        maxlower = eval
        bestlowermove = lowermove

print("EVAL BEST MOVE:", uppermove, lowermove)

"""
print("UPPER MOVES")
print(testboard.determine_capture_moves("UPPER"))
print(testboard.determine_dist_moves("UPPER"))
print(testboard.determine_slide_escape_moves("UPPER"))

print("GREEDY MOVES UPPER:", testboard.determine_greedy_moves("UPPER"))
print("GREEDY MOVES LOWER:", testboard.determine_greedy_moves("LOWER"))
"""
#for child in mctsnode.children:
    #print(child.resultsUpper)
    #print(child.resultsLower)


#test_moves(graph.root, 0)
"""
graph = Graph("UPPERS")
print(graph.root.board.generate_throws("UPPER"))

"""
# TEST one move AI here --------------------------------------------------------------------------------------
"""
singlemoveai = SillyMoveChooserAI("UPPER")
thrown_uppers = {'s': [(4, -1)], 'p': [], 'r': [(1, -1), (-3, -1), (4, -2), (2, 1)]}
thrown_lowers = {'s': [(1, 2), (-4, 4), (-1, 3)], 'p': [(-4, 3), (-2, 2), (0, 0)], 'r': []}

testboard = Board(thrown_uppers, thrown_lowers, 2, 2, 50, None)
print(testboard)
print_board(part2_to_part1(testboard))

throw, slide = singlemoveai.determine_capture_moves(testboard)
"""
"""
print(slide)
print(throw)
print(singlemoveai.get_min_distance_total(testboard))
print(singlemoveai.determine_dist_moves(testboard))""""""

"""
"""
sdanger, tdanger = singlemoveai.determine_in_danger_pieces(testboard)
print(tdanger)
print(sdanger)

print("NEXT MOVE:", singlemoveai.determine_dist_moves(testboard))

# Testing for case of throws is 1 but cant find move?
print("EMPTY BOARD TEST")
thrown_uppers = {'s':[],'p':[], 'r':[]}
thrown_lowers = {'s':[],'p':[], 'r':[]}
testboard = Board(thrown_uppers, thrown_lowers, 1, 1, 50, None)
<<<<<<< HEAD
print(testboard.generate_turns())

print(testboard.generate_turns())
"""
print("TIME TAKEN:", time.process_time() - start)
