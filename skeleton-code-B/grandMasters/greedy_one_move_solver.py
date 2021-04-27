import random

""" Function that given a board state, chooses the next "best" move. If there
are multiple, then chooses one of these best moves randomly.
"""

COUNTERS = {'s':'p', 'p':'r', 'r':'s'}
COUNTERED = {'p':'s', 'r':'p', 's':'r'}

class SillyMoveChooserAI:
    def __init__(self, player):
        self.us = player

        if player == "UPPER":
            self.opponent = "LOWER"
        else:
            self.opponent = "UPPER"

    """ Chooses next move based on criteria on the board. Doesn't look past 1 move """
    def choose_next_move(self, board):
        """ For now, play a set opening in order to gain space """
        if board.turn == 0:
            return ("THROW", "r", (-4, 0))
        if board.turn == 1:
            return ("THROW", "s", (-3, 4))
        if board.turn == 2:
            return ("THROW", "p", (-2, 2))
        if board.turn == 3:
            return ("THROW", "r", (-1, 4))
        if board.turn == 4:
            return ("THROW", "s", (0, -1))


        slide_capture_moves, throw_capture_moves = self.determine_capture_moves(board)
        # gets tiles of our pieces if our current piece is under attack from an enemy slide
        in_danger_slide, in_danger_throw = self.determine_in_danger_pieces(board)
        # gets tiles of pieces if we're in enemy throwing territory, try find a dist_closing move and escape_throw_move

        # any other productive move
        dist_closing_moves = self.determine_dist_moves(board)

        # Sift out the suicide dist_closing_moves
        # Not sure this even does anything since there doesnt seem to be suicide moves already?
        dist_closing_moves = self.remove_suicide_moves(dist_closing_moves, board)


        # Go through the potential moves in this order of priority:
        if slide_capture_moves:
            return random.choice(slide_capture_moves)
        if throw_capture_moves:
            return random.choice(throw_capture_moves)
        # Try find a move that dodges enemy slide attack and moves closer
        if in_danger_slide:
            two_in_one_moves = []
            for move in dist_closing_moves:
                for tile in in_danger_slide:
                    if move[1] == tile:
                        two_in_one_moves.append(move)

            if two_in_one_moves:
                return random.choice(two_in_one_moves)
        # try find a move for a piece that can close distance, but also dodge enemy throw
        if in_danger_throw:
            two_in_one_moves = []
            for move in dist_closing_moves:
                for tile in in_danger_throw:
                    if move[1] == tile:
                        two_in_one_moves.append(move)

            if two_in_one_moves:
                return random.choice(two_in_one_moves)

        # Otherwise just find a productive dist closing move
        if dist_closing_moves:
            return random.choice(dist_closing_moves)
        # Otherwise just play random
        return random.choice(board.generate_turns())

    """ Removes moves which result in us having one less token """
    def remove_suicide_moves(self, moves, board):
        for move in moves:
            newboard = board.apply_turn_seq(move, self.us)
            if newboard.remaining_tokens(self.us) < board.remaining_tokens(self.us):
                moves.remove(move)

        return moves

    """ Determine current moves that may be able to capture an enemy piece, if they dont move it """
    def determine_capture_moves(self, board):
        upper_moves, lower_moves = board.generate_turns()

        if self.us == "UPPER":
            own_moves = upper_moves
        else:
            own_moves = lower_moves

        #print(own_moves)
        slide_capture_moves = []
        throw_capture_moves = []
        for move in own_moves:
            next_board = board.apply_turn_seq(move, self.us)
            if next_board.remaining_tokens(self.opponent) < board.remaining_tokens(self.opponent):
                if move[0] == "THROW":
                    throw_capture_moves.append(move)
                else:
                    slide_capture_moves.append(move)

        return slide_capture_moves, throw_capture_moves

    """ Determine current pieces that are in danger, return these tiles """
    def determine_in_danger_pieces(self, board):
        # determine which pieces we got
        if self.us == "UPPER":
            our_pieces = board.thrown_uppers
            enemy_pieces = board.thrown_lowers
        else:
            our_pieces = board.thrown_lowers
            enemy_pieces = board.thrown_uppers

        slide_danger = []
        throw_danger = []
        # Determine in danger by enemy slides, ie find pieces with their counter distance 1
        for key in our_pieces.keys():
            if enemy_pieces[COUNTERED[key]]:
                for tile in our_pieces[key]:
                    # Determine if theres an adjacent enemy counter piece
                    for tile2 in enemy_pieces[COUNTERED[key]]:
                        if self.distance(tile, tile2) == 1:
                            slide_danger.append(tile)
                    # Determine whether the current tile is in enemy throw territory

                    if self.us == "UPPER":
                        if tile[0] < (-4 + 9 - board.unthrown_lowers):
                            throw_danger.append(tile)
                    if self.us == "LOWER":
                        if tile[0] > (4 - 9 + board.unthrown_uppers):
                            throw_danger.append(tile)
        return slide_danger, throw_danger

    # Determines moves that close distance from one piece to its counter
    # Doesn't consider slide capture moves. Would've been picked up by determine capture moves
    def determine_dist_moves(self, board):
        upper_moves, lower_moves = board.generate_turns()

        if self.us == "UPPER":
            own_moves = upper_moves
        else:
            own_moves = lower_moves

        dist_moves = []
        for move in own_moves:
            next_board = board.apply_turn_seq(move, self.us)
            if self.get_min_distance_total(next_board) < self.get_min_distance_total(board):
                # Only use slide moves to close dist, don't throw
                if move[0] == "SLIDE":
                    dist_moves.append(move)

        return dist_moves

    # Functions from assignment 1
    def distance(self, coord1, coord2):
        (r1, c1) = coord1
        (r2, c2) = coord2

        dr = r1 - r2
        dc = c1 - c2
        if (dr < 0 and dc < 0) or (dr > 0 and dc > 0):
            return abs(dr + dc)
        else:
            return max(abs(dr), abs(dc))

    # Returns total of min distance of every piece to its counter
    # This min distance effectively just focusses on the min distnace pairing
    def get_min_distance_total(self, board):
        # determine which pieces we got
        if self.us == "UPPER":
            our_pieces = board.thrown_uppers
            enemy_pieces = board.thrown_lowers
        else:
            our_pieces = board.thrown_lowers
            enemy_pieces = board.thrown_uppers

        total = 0

        # For each piecetype in our_pieces find its min distance to an enemy
        for key in our_pieces.keys():
            if enemy_pieces[COUNTERS[key]]:
                # If enemy piece exists for our piece, go through all pairings of tiles and find the min dist
                mindist = 100000
                for tile in our_pieces[key]:
                    for tile2 in enemy_pieces[COUNTERS[key]]:
                        dist = self.distance(tile, tile2)
                        if dist < mindist:
                            mindist = dist
            # If no enemies found, add 0
            else:
                mindist = 0

            total += mindist
        return total
