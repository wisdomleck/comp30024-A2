from graph import Graph
import random


random.seed()
def test_moves(root, depth):
    if depth > 10:
        return
    print(root.board)
    adjacents = root.adjacent_nodes()
    rand_pick = random.randint(0, len(adjacents))
    test_moves(adjacents[rand_pick], depth + 1)

graph = Graph("UPPERS")
test_moves(graph.root, 0)
