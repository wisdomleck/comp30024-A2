from graph import Graph
from evaluation import classify_board, thrown_diff, unthrown_diff, dominance_diff, spread_diff, capture_dist_difference
import numpy as np
import time

start = time.process_time()

graph = Graph("UPPER")
boards = graph.data_collection()
data = []
for board, value in boards:
    board_class = classify_board(board)
    t_diff = thrown_diff(board)
    ut_diff = unthrown_diff(board)
    dom_diff = dominance_diff(board)
    s_diff = spread_diff(board)
    c_diff = capture_dist_difference(board)
    data.append([board_class, t_diff, ut_diff, dom_diff, s_diff, c_diff, value])

np.savetxt("board_data.csv", data, fmt = "%s", delimiter=",")

print("BOARDS EVALUATED: ", len(boards) )
print("TIME TAKEN:", time.process_time() - start)
