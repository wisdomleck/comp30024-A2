from graph import Graph
from evaluation import thrown_diff, unthrown_diff, dominance_diff, spread

graph = Graph("UPPER")
data = graph.data_collection()
for board, value in data:
    print(board)
    print(value)
