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

def unthrown_diff(board):
    return board.unthrown_uppers - board.unthrown_lowers

def thrown_diff(board):
    return board.remaining_tokens("UPPER") - board.remaining_tokens("LOWER") - unthrown_diff(board)

def dominance_diff(board):
    up_rps = (len(board.thrown_uppers["r"]), len(board.thrown_uppers["p"]), len(board.thrown_uppers["s"]))
    low_rps = (len(board.thrown_lowers["r"]), len(board.thrown_lowers["p"]), len(board.thrown_lowers["s"]))

    up_r = up_rps[0]/(low_rps[1] + up_rps[0] + 1)
    up_p = up_rps[1]/(low_rps[2] + up_rps[1] + 1)
    up_s = up_rps[2]/(low_rps[0] + up_rps[2] + 1)

    low_r = low_rps[0]/(up_rps[1] + low_rps[0] + 1)
    low_p = low_rps[1]/(up_rps[2] + low_rps[1] + 1)
    low_s = low_rps[2]/(up_rps[0] + low_rps[2] + 1)
    return (up_r + up_p + up_s) - (low_r + low_p + low_s)

def spread(ps):
    if not ps:
        return 0
    mean = np.mean(ps, axis = 0)
    centroid =  (round(mean[0]), round(mean[1]))
    return sum([distance(p, centroid) for p in ps])/len(ps)

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

    # Features: throw_diff, scissor_diff, paper_diff, rock_diff, median row
    ut_diff = unthrown_diff(board)
    t_diff = thrown_diff(board)
    dom_diff = dominance_diff(board)
    s_diff = spread_diff(board)
    c_diff = capture_dist_difference(board)
    #print(unthrown_diff, dom_diff, thrown_diff)
    value = 0.2 * ut_diff + 0.2*t_diff + 0.25*dom_diff + 0.05*s_diff + 0.05*c_diff
    capped_val = min(max(value, -1), 1)

    return capped_val

def evaluate_move(board, move, player):
    return evaluate(apply_move(board, move, player))

def apply_move(board, move, player):
    player_thrown, player_unthrown = board.player_pieces(player)
    opponent_thrown, opponent_unthrown = board.opponent_pieces(player)
    player_thrown = board.copy_dict(player_thrown)
    opponent_thrown = board.copy_dict(opponent_thrown)

    if move[0] == "THROW":
        t = board.update_throw(player_thrown, move[1], move[2])
        player_unthrown -= 1
    else:
        t = board.update_slide_swing(player_thrown, move[1], move[2])

    counters_t = COUNTERED[t]
    countered_t = COUNTERS[t]

    if move[2] in player_thrown[counters_t] or move[2] in opponent_thrown[counters_t]:
        player_thrown[t] = [p for p in player_thrown[t] if p != move[2]]

    player_thrown[countered_t] = [p for p in player_thrown[countered_t] if p != move[2]]
    opponent_thrown[countered_t] = [p for p in opponent_thrown[countered_t] if p != move[2]]

    if player == "UPPER":
        return Board(player_thrown, opponent_thrown, player_unthrown, opponent_unthrown, board.turn + 1, None)
    else:
        return Board(opponent_thrown, player_thrown, opponent_unthrown, player_unthrown, board.turn + 1, None)
