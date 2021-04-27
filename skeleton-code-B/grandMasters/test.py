from graph import Graph
from board import Board
from MCTS import MCTSNode

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
"""
