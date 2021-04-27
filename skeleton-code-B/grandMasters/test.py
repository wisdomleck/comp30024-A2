from graph import Graph
from board import Board
from MCTS import MCTSNode
from util import print_board, print_slide, print_swing, reformat_board, part2_to_part1, part1_to_part2
import random

random.seed()
"""def test_moves(root, depth):
    if depth > 10:
        return
    print(root.board)
    adjacents = root.adjacent_nodes()
    rand_pick = random.randint(0, len(adjacents))
    test_moves(adjacents[rand_pick], depth + 1)"""


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
for i in range(1):
    result, turns = mctsnode.rollout()
    if result == 1:
        upper_wins += 1
    elif result == -1:
        lower_wins += 1
    else:
        ties += 1
    total_turns += turns
    total_value += result
print(f"UpperWins: {upper_wins}\nLowerWins: {lower_wins}\nTies: {ties}\nAvgTurnsNeeded: {total_turns/1}")
print(total_value)

#test_moves(graph.root, 0)

"""
graph = Graph("UPPERS")
print(graph.root.board.generate_throws("UPPER"))
"""
