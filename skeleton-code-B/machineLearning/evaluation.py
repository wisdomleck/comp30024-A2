from board import Board
import numpy as np

COUNTERS = {'s':'p', 'p':'r', 'r':'s'}
COUNTERED = {'p':'s', 'r':'p', 's':'r'}

def distance(coord1, coord2):
    (r1, c1) = coord1
    (r2, c2) = coord2

    dr = r1 - r2
    dc = c1 - c2
    if (dr < 0 and dc < 0) or (dr > 0 and dc > 0):
        return abs(dr + dc)
    else:
        return max(abs(dr), abs(dc))

def classify_board(board):
    rem_u = board.remaining_tokens("UPPER")
    rem_l = board.remaining_tokens("LOWER")
    if rem_u >= 7 and rem_l >= 7:
        return "OPENING"
    if (rem_u >= 4 and rem_u >= 4 and rem_u < 7) or (rem_l >= 4 and rem_u >= 4 and rem_u < 7):
        return "MID GAME"
    return "END GAME"

def unthrown_diff(board):
    return board.unthrown_uppers - board.unthrown_lowers

def thrown_diff(board):
    return board.remaining_tokens("UPPER") - board.remaining_tokens("LOWER") - unthrown_diff(board)

def dominance_diff(board):
    up_rps = (len(board.thrown_uppers["r"]), len(board.thrown_uppers["p"]), len(board.thrown_uppers["s"]))
    low_rps = (len(board.thrown_lowers["r"]), len(board.thrown_lowers["p"]), len(board.thrown_lowers["s"]))

    up_r = up_rps[0]/(low_rps[1] + 1)
    up_p = up_rps[1]/(low_rps[2] + 1)
    up_s = up_rps[2]/(low_rps[0] + 1)

    low_r = low_rps[0]/(up_rps[1] + 1)
    low_p = low_rps[1]/(up_rps[2] + 1)
    low_s = low_rps[2]/(up_rps[0] + 1)
    return (up_r + up_p + up_s) - (low_r + low_p + low_s)

def centroid(ps):
    mean = np.mean(ps, axis = 0)
    return (round(mean[0]), round(mean[1]))

def spread(ps):
    if not ps:
        return 0
    c = centroid(ps)
    return sum([distance(p, c) for p in ps])/len(ps)

def spread_diff(board):
    u_ps = board.chain(board.thrown_uppers)
    l_ps = board.chain(board.thrown_lowers)
    return spread(u_ps) - spread(l_ps)

def min_circuit(ps, qs):
    # Number of tiles on the board
    min_circuit_dist = 9
    for p in ps:
        dists = [distance(p, q) for q in qs]

        if not dists:
            return 0

        avg_dist = np.sum(dists)/len(dists)
        if avg_dist < min_circuit_dist:
            min_circuit_dist = avg_dist
    return min_circuit_dist

def sum_min_dists(player_thrown, opponent_thrown):
    sum_dists = 0
    for key, value in player_thrown.items():
        countered = opponent_thrown[COUNTERS[key]]
        sum_dists += min_circuit(value, countered)
    return sum_dists

def capture_dist_difference(board):
    return sum_min_dists(board.thrown_lowers, board.thrown_uppers) - sum_min_dists(board.thrown_uppers, board.thrown_lowers)

# evaluates a board state with the option of evaluating after input move from input
def evaluate(board):
    if board.is_win("UPPER"):
        return 1
    if board.is_win("LOWER"):
        return -1
    if board.is_draw():
        return 0
