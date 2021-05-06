from grandMasters.board import Board

"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This module contains some helper functions for printing actions and boards.
Feel free to use and/or modify them to help you develop your program.
"""
def print_slide(t, r_a, q_a, r_b, q_b, **kwargs):
    """
    Output a slide action for turn t of a token from hex (r_a, q_a)
    to hex (r_b, q_b), according to the format instructions.

    Any keyword arguments are passed through to the print function.
    """
    print(f"Turn {t}: SLIDE from {(r_a, q_a)} to {(r_b, q_b)}", **kwargs)


def print_swing(t, r_a, q_a, r_b, q_b, **kwargs):
    """
    Output a swing action for turn t of a token from hex (r_a, q_a)
    to hex (r_b, q_b), according to the format instructions.

    Any keyword arguments are passed through to the print function.
    """
    print(f"Turn {t}: SWING from {(r_a, q_a)} to {(r_b, q_b)}", **kwargs)


def print_board(board_dict, message="", compact=True, ansi=False, **kwargs):
    """
    For help with visualisation and debugging: output a board diagram with
    any information you like (tokens, heuristic values, distances, etc.).

    Arguments:

    board_dict -- A dictionary with (r, q) tuples as keys (following axial
        coordinate system from specification) and printable objects (e.g.
        strings, numbers) as values.
        This function will arrange these printable values on a hex grid
        and output the result.
        Note: At most the first 5 characters will be printed from the string
        representation of each value.
    message -- A printable object (e.g. string, number) that will be placed
        above the board in the visualisation. Default is "" (no message).
    ansi -- True if you want to use ANSI control codes to enrich the output.
        Compatible with terminals supporting ANSI control codes. Default
        False.
    compact -- True if you want to use a compact board visualisation,
        False to use a bigger one including axial coordinates along with
        the printable information in each hex. Default True (small board).

    Any other keyword arguments are passed through to the print function.

    Example:

        >>> board_dict = {
        ...     ( 0, 0): "hello",
        ...     ( 0, 2): "world",
        ...     ( 3,-2): "(p)",
        ...     ( 2,-1): "(S)",
        ...     (-4, 0): "(R)",
        ... }
        >>> print_board(board_dict, "message goes here", ansi=False)
        # message goes here
        #              .-'-._.-'-._.-'-._.-'-._.-'-.
        #             |     |     |     |     |     |
        #           .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
        #          |     |     | (p) |     |     |     |
        #        .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
        #       |     |     |     | (S) |     |     |     |
        #     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
        #    |     |     |     |     |     |     |     |     |
        #  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
        # |     |     |     |     |hello|     |world|     |     |
        # '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #    |     |     |     |     |     |     |     |     |
        #    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #       |     |     |     |     |     |     |     |
        #       '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #          |     |     |     |     |     |     |
        #          '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #             | (R) |     |     |     |     |
        #             '-._.-'-._.-'-._.-'-._.-'-._.-'
    """
    if compact:
        template = """# {00:}
#              .-'-._.-'-._.-'-._.-'-._.-'-.
#             |{57:}|{58:}|{59:}|{60:}|{61:}|
#           .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#          |{51:}|{52:}|{53:}|{54:}|{55:}|{56:}|
#        .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#       |{44:}|{45:}|{46:}|{47:}|{48:}|{49:}|{50:}|
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{36:}|{37:}|{38:}|{39:}|{40:}|{41:}|{42:}|{43:}|
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{27:}|{28:}|{29:}|{30:}|{31:}|{32:}|{33:}|{34:}|{35:}|
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{19:}|{20:}|{21:}|{22:}|{23:}|{24:}|{25:}|{26:}|
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{12:}|{13:}|{14:}|{15:}|{16:}|{17:}|{18:}|
#       '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{06:}|{07:}|{08:}|{09:}|{10:}|{11:}|
#          '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#             |{01:}|{02:}|{03:}|{04:}|{05:}|
#             '-._.-'-._.-'-._.-'-._.-'-._.-'"""
    else:
        template = """# {00:}
#                  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#                 | {57:} | {58:} | {59:} | {60:} | {61:} |
#                 |  4,-4 |  4,-3 |  4,-2 |  4,-1 |  4, 0 |
#              ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#             | {51:} | {52:} | {53:} | {54:} | {55:} | {56:} |
#             |  3,-4 |  3,-3 |  3,-2 |  3,-1 |  3, 0 |  3, 1 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {44:} | {45:} | {46:} | {47:} | {48:} | {49:} | {50:} |
#         |  2,-4 |  2,-3 |  2,-2 |  2,-1 |  2, 0 |  2, 1 |  2, 2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#     | {36:} | {37:} | {38:} | {39:} | {40:} | {41:} | {42:} | {43:} |
#     |  1,-4 |  1,-3 |  1,-2 |  1,-1 |  1, 0 |  1, 1 |  1, 2 |  1, 3 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {27:} | {28:} | {29:} | {30:} | {31:} | {32:} | {33:} | {34:} | {35:} |
# |  0,-4 |  0,-3 |  0,-2 |  0,-1 |  0, 0 |  0, 1 |  0, 2 |  0, 3 |  0, 4 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#     | {19:} | {20:} | {21:} | {22:} | {23:} | {24:} | {25:} | {26:} |
#     | -1,-3 | -1,-2 | -1,-1 | -1, 0 | -1, 1 | -1, 2 | -1, 3 | -1, 4 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#         | {12:} | {13:} | {14:} | {15:} | {16:} | {17:} | {18:} |
#         | -2,-2 | -2,-1 | -2, 0 | -2, 1 | -2, 2 | -2, 3 | -2, 4 |
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#             | {06:} | {07:} | {08:} | {09:} | {10:} | {11:} |
#             | -3,-1 | -3, 0 | -3, 1 | -3, 2 | -3, 3 | -3, 4 |   key:
#              `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'     ,-' `-.
#                 | {01:} | {02:} | {03:} | {04:} | {05:} |       | input |
#                 | -4, 0 | -4, 1 | -4, 2 | -4, 3 | -4, 4 |       |  r, q |
#                  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'         `-._,-'"""
    # prepare the provided board contents as strings, formatted to size.
    ran = range(-4, +4+1)
    cells = []
    for rq in [(r,q) for r in ran for q in ran if -r-q in ran]:
        if rq in board_dict:
            cell = str(board_dict[rq]).center(5)
            if ansi:
                # put contents in bold
                cell = f"\033[1m{cell}\033[0m"
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)
    # prepare the message, formatted across multiple lines
    multiline_message = "\n# ".join(message.splitlines())
    # fill in the template to create the board drawing, then print!
    board = template.format(multiline_message, *cells)
    print(board, **kwargs)



""" Reformats the input json file into a dict to be used by other functions. Dict
is in form of coordinates as values, piece as key.
(r,q) : piece
"""

def reformat_board(board):
    reformatted_board = {}
    for unit, pieces in board.items():
        for piece in pieces:
             position = (piece[1], piece[2])
             if unit == "upper":
                 reformatted_board[position] = piece[0].upper()
             elif unit == "lower":
                 reformatted_board[position] = piece[0]
             else:
                 reformatted_board[position] = "B"
    return reformatted_board


""" Converts a board in the format in part 2 into a board in part 1 just for printing
purposes. Ignore number of throws

!!!!! NOTE: For boards with multiple pieces on one tile i.e Upper s and Lower s on same tile,
part1 board doesn't account for this scenario
"""

def part2_to_part1(board):
    outputboard = {}
    # Get coords of lower pieces
    for key, value in board.thrown_lowers.items():
        if key == "r" and board.thrown_lowers[key]:
            for tile in board.thrown_lowers[key]:
                outputboard[tile] = "r"
        if key == "s" and board.thrown_lowers[key]:
            for tile in board.thrown_lowers[key]:
                outputboard[tile] = "s"
        if key == "p" and board.thrown_lowers[key]:
            for tile in board.thrown_lowers[key]:
                outputboard[tile] = "p"
    # Get coords of uppwer pieces
    for key, value in board.thrown_uppers.items():
        if key == "r" and board.thrown_uppers[key]:
            for tile in board.thrown_uppers[key]:
                outputboard[tile] = "R"
        if key == "s" and board.thrown_uppers[key]:
            for tile in board.thrown_uppers[key]:
                outputboard[tile] = "S"
        if key == "p" and board.thrown_uppers[key]:
            for tile in board.thrown_uppers[key]:
                outputboard[tile] = "P"

    return outputboard

""" Converts a board in the format in part 1 into a board in part 2 just for printing
purposes. Ignore number of throws. Here, set unthrowns to 0, and fill in rest of parameters with default values
"""

def part1_to_part2(board):
    thrown_uppers = {'s':[],'p':[], 'r':[]}
    thrown_lowers = {'s':[],'p':[], 'r':[]}

    for key, value in board.items():
        if value == "R":
            thrown_uppers['r'].append(key)
        elif value == "S":
            thrown_uppers['s'].append(key)
        elif value == "P":
            thrown_uppers['p'].append(key)
        elif value == "r":
            thrown_lowers['r'].append(key)
        elif value == "s":
            thrown_lowers['s'].append(key)
        elif value == "p":
            thrown_lowers['p'].append(key)

    return Board(thrown_uppers, thrown_lowers, 0, 0, 0, None)
