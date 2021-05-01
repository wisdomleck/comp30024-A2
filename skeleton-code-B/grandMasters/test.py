from graph import Graph
from board import Board
from MCTS import MCTSNode
from util import print_board, print_slide, print_swing, reformat_board, part2_to_part1, part1_to_part2
import random
from greedy_one_move_solver import SillyMoveChooserAI

random.seed()
def test_moves(root, depth):
    if depth > 10:
        return
    print(root.board)
    adjacents = root.adjacent_nodes()
    #rand_pick = random.randint(0, len(adjacents))
    test_moves(random.choice(adjacents), depth + 1)

#newgraph = Graph("UPPER")
#test_moves(newgraph.root, 0)
# ISWIN ISDRAW TESTING HERE --------------------------------------------------------------------------------
"""
uppers = {'s':[(0,1)],'p':[], 'r':[]}
lowers = {'s':[(0,0)],'p':[], 'r':[]}
testboard = Board(uppers, lowers, 0, 0, 0, None)

print(testboard.is_win("UPPER"))
print(testboard.is_draw())
"""
# apply_turn2 TESTING HERE ---------------------------------------------------------------------------------
"""
uppers = {'s':[],'p':[], 'r':[]}
lowers = {'s':[],'p':[], 'r':[]}

testboard = Board(uppers, lowers, 9, 9, 0, None)

print(testboard)

testboard = testboard.apply_turn2((("THROW"), "r", (0,0)), ("THROW", "p", (0,1)))
testboard = testboard.apply_turn2((("THROW"), "s", (-1, 1)), ("SLIDE", (0,1), (-1,1)))

print(testboard)
"""
# MCTS TESTING HERE ----------------------------------------------------------------------------------------


graph = Graph("UPPERS")

board = graph.root.board

print(board)
print_board(part2_to_part1(board))
print(part1_to_part2(part2_to_part1(board)))

mctsnode = MCTSNode(board, "UPPER")

upper_wins = 0
lower_wins = 0
ties = 0
total_turns = 0

total_value = 0
for i in range(100):
    result, turns = mctsnode.rollout()
    if result == 1:
        upper_wins += 1
    elif result == -1:
        lower_wins += 1
    else:
        ties += 1
    total_turns += turns
    total_value += result
print(f"UpperWins: {upper_wins}\nLowerWins: {lower_wins}\nTies: {ties}\nAvgTurnsNeeded: {total_turns/100}")
print(total_value)

#test_moves(graph.root, 0)

"""
graph = Graph("UPPERS")
print(graph.root.board.generate_throws("UPPER"))


# TEST one move AI here --------------------------------------------------------------------------------------
""""""
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

sdanger, tdanger = singlemoveai.determine_in_danger_pieces(testboard)
print(tdanger)
print(sdanger)

print("NEXT MOVE:", singlemoveai.determine_dist_moves(testboard))

# Testing for case of throws is 1 but cant find move?
print("EMPTY BOARD TEST")
thrown_uppers = {'s':[],'p':[], 'r':[]}
thrown_lowers = {'s':[],'p':[], 'r':[]}
testboard = Board(thrown_uppers, thrown_lowers, 1, 1, 50, None)
print(testboard.generate_turns()) """
