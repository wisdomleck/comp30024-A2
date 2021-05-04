from itertools import product, chain
from copy import deepcopy

COUNTERS = {'s':'p', 'p':'r', 'r':'s'}
COUNTERED = {'p':'s', 'r':'p', 's':'r'}

SLIDE_DIRECTIONS = [(0,1), (-1,1), (-1,0), (0,-1), (1,-1), (1,0)]
class Board:
    def __init__(self, thrown_uppers, thrown_lowers, unthrown_uppers, unthrown_lowers, turn, move):
        # Dictionaries to hold upper and lower pieces. Key: piece types, value: positions
        self.thrown_uppers = thrown_uppers
        self.thrown_lowers = thrown_lowers

        # Integer count of number of tokens available to throw
        self.unthrown_uppers = unthrown_uppers
        self.unthrown_lowers = unthrown_lowers

        # Number of turns played to reach current board
        self.turn = turn
        # Move played to reach this board
        self.move = move

    def __eq__(self, other):
        return self.thrown_uppers == other.thrown_uppers and\
        self.thrown_lowers == other.thrown_lowers and\
        self.unthrown_uppers == other.unthrown_uppers and\
        self.unthrown_lowers == other.unthrown_lowers

    def __str__(self):
        return f"Thrown Uppers: {self.thrown_uppers}\nUnthrown Uppers: {self.unthrown_uppers}\nThrown Lowers: {self.thrown_lowers}\nUnthrown Lowers: {self.unthrown_uppers}\nMove:{self.move}\n"

    def is_win(self, player):
        other = "LOWER" if player == "UPPER" else "UPPER"

        return self.remaining_tokens(player) and not self.remaining_tokens(other) or\
        self.has_invincible(player) and\
        not self.has_invincible(other) and\
        self.remaining_tokens(other) == 1

    def is_draw(self):
        return (not self.remaining_tokens("UPPER") and not self.remaining_tokens("LOWER")) or\
        self.has_invincible("UPPER") and self.has_invincible("LOWER") or self.turn >= 360

    """ Returns the result of the game, from the perspective of the current board.
        Denote:
        1 - win for UPPER
        0 - tie
        -1 - win for LOWER
    """
    def game_result(self):
        if self.is_win("UPPER"):
            return 1
        elif self.is_win("LOWER"):
            return -1

        if self.is_draw():
            return 0
        # If somehow this gets triggered
        return 7777


    def remaining_tokens(self, player):
        if player == "UPPER":
            return len(list(chain.from_iterable(self.thrown_uppers.values()))) + self.unthrown_uppers
        else:
            return len(list(chain.from_iterable(self.thrown_lowers.values()))) + self.unthrown_lowers

    def has_invincible(self,player):
        if player == "UPPER":
            player_throws = self.thrown_uppers
            other_throws = self.thrown_lowers
            other_unthrown = self.unthrown_lowers
        else:
            player_throws = self.thrown_lowers
            other_throws = self.thrown_uppers
            other_unthrown = self.unthrown_uppers

        for key, value in player_throws.items():
            if value and not other_throws[COUNTERED[key]] and not other_unthrown:
                return True
        return False



    """ NEED TO HANDLE CAPTURES FOR update FUNCTIONS """

    """ Updates the corresponding dictionary with a slide or swing move """
    def update_slide_swing(self, dict, from_coord, to_coord):
        for key in dict.keys():
            for tile in dict[key]:
                if tile == from_coord:
                    dict[key].remove(from_coord)
                    dict[key].append(to_coord)
                    return key

    """ Updates the dictionary with a throw move """
    def update_throw(self, dict, piece, to):
        dict[piece].append(to)
        return piece

    """ After the simultaneous move, resolve any captures that occurred """
    """ pass in moves that were made that turn """
    def resolve_conflicts(self, upper_thrown, lower_thrown, upper_move, lower_move):
        # Upper_move, lower_move in form of (piecetype, newcoord)
        upper_piecetype = upper_move[0]
        upper_newcoord = upper_move[1]
        lower_piecetype = lower_move[0]
        lower_newcoord = lower_move[1]

        # Pieces to remove
        remove_list_upper = set()
        remove_list_lower = set()

        # See if upper_move or lower_move is a suicide or not
        if upper_newcoord in upper_thrown[COUNTERED[upper_piecetype]]:
            remove_list_upper.add((upper_piecetype, upper_newcoord))
        if upper_newcoord in lower_thrown[COUNTERED[upper_piecetype]]:
            remove_list_upper.add((upper_piecetype, upper_newcoord))

        #print("LOWER PIECETYPE", lower_piecetype)
        #print("LOWER_MOVE: ", lower_move)
        if lower_newcoord in upper_thrown[COUNTERED[lower_piecetype]]:
            remove_list_lower.add((lower_piecetype, lower_newcoord))
        if lower_newcoord in lower_thrown[COUNTERED[lower_piecetype]]:
            remove_list_lower.add((lower_piecetype, lower_newcoord))

        # See if upper_move or lower_move captured anything or not
        if upper_newcoord in upper_thrown[COUNTERS[upper_piecetype]]:
            remove_list_upper.add((COUNTERS[upper_piecetype], upper_newcoord))
        if upper_newcoord in lower_thrown[COUNTERS[upper_piecetype]]:
            remove_list_lower.add((COUNTERS[upper_piecetype], upper_newcoord))

        if lower_newcoord in upper_thrown[COUNTERS[lower_piecetype]]:
            remove_list_upper.add((COUNTERS[lower_piecetype], lower_newcoord))
        if lower_newcoord in lower_thrown[COUNTERS[lower_piecetype]]:
            remove_list_lower.add((COUNTERS[lower_piecetype], lower_newcoord))


        # Remove these pieces that are captured
        for element in remove_list_upper:
            # Case for multiple instances of same piece on same tile
            while element[1] in upper_thrown[element[0]]:
                upper_thrown[element[0]].remove(element[1])

        for element in remove_list_lower:
            # Case for multiple instances of same piece on same tile
            while element[1] in lower_thrown[element[0]]:
                lower_thrown[element[0]].remove(element[1])

        # Return these updated dictionaries
        return upper_thrown, lower_thrown

    """ Apply a upper and lower move to the board """
    def apply_turn2(self, upper_move, lower_move):
        # Create deepcopy of token related variables
        new_thrown_uppers = deepcopy(self.thrown_uppers)
        new_thrown_lowers = deepcopy(self.thrown_lowers)
        unthrown_uppers = self.unthrown_uppers
        unthrown_lowers = self.unthrown_lowers

        # For upper's move
        # Slide or swing
        if upper_move[0] != "THROW":
            coord_from = upper_move[1]
            coord_to = upper_move[2]
            upper_piecetype = self.update_slide_swing(new_thrown_uppers, coord_from, coord_to)
        # Throw
        else:
            upper_piecetype = self.update_throw(new_thrown_uppers, upper_move[1], upper_move[2])
            unthrown_uppers -= 1

        # For lower's move:
        # Slide or swing
        if lower_move[0] != "THROW":
            coord_from = lower_move[1]
            coord_to = lower_move[2]
            lower_piecetype = self.update_slide_swing(new_thrown_lowers, coord_from, coord_to)
        # Throw
        else:
            lower_piecetype = self.update_throw(new_thrown_lowers, lower_move[1], lower_move[2])
            unthrown_lowers -= 1

        new_thrown_uppers, new_thrown_lowers = self.resolve_conflicts(new_thrown_uppers, new_thrown_lowers, (upper_piecetype, upper_move[2]), (lower_piecetype, lower_move[2]))
        return Board(new_thrown_uppers, new_thrown_lowers, unthrown_uppers, unthrown_lowers, self.turn+1, (upper_move, lower_move))

    """ Single move at a time """
    def apply_turn_seq(self, move, player):
        # Create deepcopy of token related variables
        new_thrown_uppers = deepcopy(self.thrown_uppers)
        new_thrown_lowers = deepcopy(self.thrown_lowers)
        unthrown_uppers = self.unthrown_uppers
        unthrown_lowers = self.unthrown_lowers

        """
        Given a move and a player, execute that move for that player
        """
        if player == "UPPER":
            if move[0] != "THROW":
                coord_from = move[1]
                coord_to = move[2]
                upper_piecetype = self.update_slide_swing(new_thrown_uppers, coord_from, coord_to)
            # Throw
            else:
                upper_piecetype = self.update_throw(new_thrown_uppers, move[1], move[2])
                unthrown_uppers -= 1

        elif player == "LOWER":
            if move[0] != "THROW":
                coord_from = move[1]
                coord_to = move[2]
                lower_piecetype = self.update_slide_swing(new_thrown_lowers, coord_from, coord_to)
            # Throw
            else:
                lower_piecetype = self.update_throw(new_thrown_lowers, move[1], move[2])
                unthrown_lowers -= 1

        # Hacky method to update move for only one player
        if player == "UPPER":
            new_thrown_uppers, new_thrown_lowers = self.resolve_conflicts(new_thrown_uppers, new_thrown_lowers, (upper_piecetype, move[2]), ("r", (5,5))) # impossible lower move
        elif player == "LOWER":
            new_thrown_uppers, new_thrown_lowers = self.resolve_conflicts(new_thrown_uppers, new_thrown_lowers, ("r", (5,5)), (lower_piecetype, move[2])) # impossible upper move
        return Board(new_thrown_uppers, new_thrown_lowers, unthrown_uppers, unthrown_lowers, self.turn+1, None)





    """ GENERATE GREEDY MOVESETS FOR MCTS """
    """ make a function that returns a list of moves by priority? then take first x?"""
    """ Determines capture moves for a player """
    """ Problems list:
        - can jitter due to escaping slide then closing distance
        - doesn't prioritise any moves over the other (just need random for mcts)
    """

    """ determines greedy moves for both """
    def determine_greedy_moves(self):
        moves = []

        all_moves = self.generate_turns()

        #throw_captures, slide_captures = self.determine_capture_moves(player, all_moves)
        #moves += throw_captures + slide_captures
        #moves += self.determine_dist_moves(player, all_moves)
        #moves += self.determine_slide_escape_moves(player)
        #moves = self.remove_suicide_moves(moves, player)

        if not moves:
            if player == "UPPER":
                return all_moves[0]
            else:
                return all_moves[1]
        return moves

    def determine_capture_moves(self, player, all_moves):

        upper_moves, lower_moves = all_moves

        if player == "UPPER":
            opponent = "LOWER"
            own_moves = upper_moves
        else:
            opponent = "UPPER"
            own_moves = lower_moves

        #print(own_moves)
        slide_capture_moves = []
        throw_capture_moves = []

        #print("UPPER:", self.thrown_uppers)
        #print("LOWER:", self.thrown_lowers)
        #print(own_moves)
        for move in own_moves:
            next_board = self.apply_turn_seq(move, player)
            if next_board.remaining_tokens(opponent) < self.remaining_tokens(opponent):
                if move[0] == "THROW":
                    throw_capture_moves.append(move)
                else:
                    slide_capture_moves.append(move)

        return slide_capture_moves, throw_capture_moves

    def determine_dist_moves(self, player, all_moves):
        upper_moves, lower_moves = all_moves

        if player == "UPPER":
            own_moves = upper_moves
        else:
            own_moves = lower_moves

        dist_moves = []
        for move in own_moves:
            next_board = self.apply_turn_seq(move, player)
            if next_board.get_min_distance_total(player) < self.get_min_distance_total(player):
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
    def get_min_distance_total(self, player):
        # determine which pieces we got
        if player == "UPPER":
            our_pieces = self.thrown_uppers
            enemy_pieces = self.thrown_lowers
        else:
            our_pieces = self.thrown_lowers
            enemy_pieces = self.thrown_uppers

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

    """ Removes suicide moves from our moveset """
    def remove_suicide_moves(self, moves, player):
        for move in moves:
            newboard = self.apply_turn_seq(move, player)
            if newboard.remaining_tokens(player) < self.remaining_tokens(player):
                moves.remove(move)

        return moves

    """ Determine current pieces that are in danger, return these tiles """
    def determine_slide_escape_moves(self, player):
        # determine which pieces we got
        if player == "UPPER":
            our_pieces = self.thrown_uppers
            enemy_pieces = self.thrown_lowers
        else:
            our_pieces = self.thrown_lowers
            enemy_pieces = self.thrown_uppers

        escape_moves = []
        available_tiles = [(r,q) for r in range(-4,5) for q in range(-4,5) if -r-q in range(-4,5)]
        # Determine in danger by enemy slides, ie find pieces with their counter distance 1
        for key in our_pieces.keys():
            if enemy_pieces[COUNTERED[key]]:
                for tile in our_pieces[key]:
                    # Determine if theres an adjacent enemy counter piece
                    for tile2 in enemy_pieces[COUNTERED[key]]:
                        if self.distance(tile, tile2) == 1:
                            # Find a move that increases distance to 2
                            for direction in SLIDE_DIRECTIONS:
                                newtile = (tile[0] + direction[0], tile[1] + direction[1])
                                if newtile not in available_tiles:
                                    continue
                                elif self.distance(newtile, tile2) == 2:
                                    escape_moves.append(("SLIDE", tile, newtile))

        return escape_moves



    def generate_turns(self):
        """
        Generate all possible turns in the current board state where a turn
        is a 3-tuple as defined in the part B specs. The set of turns includes
        all possible combinations of throw, slide and swing moves playable by
        upper and lower.
        """
        lower_moves = self.generate_throws("LOWER")
        lower_moves += self.generate_slides(self.thrown_lowers)
        lower_moves += self.generate_swings(self.thrown_lowers)

        upper_moves = self.generate_throws("UPPER")
        upper_moves += self.generate_slides(self.thrown_uppers)
        upper_moves += self.generate_swings(self.thrown_uppers)
        #print(len(lower_moves), len(upper_moves))
        return upper_moves, lower_moves

    def generate_throws(self, player):
        """
        Generate all possible throw moves for the given player, accounting for
        restricted area based on turn and restricted number of throws.
        """
        ran_q = range(-4,5)

        throws = []
        if player == "UPPER":
            # Return empty list if throws are exhausted.
            if self.unthrown_uppers == 0:
                return throws
            # Restrict r axis range based off UNTHROWN TOKENS.
            min_r = max(-4, 4 - (9 - self.unthrown_uppers))
            ran_r = range(min_r, 5)

        else:
            # Return empty list if throws are exhausted.
            if self.unthrown_lowers == 0:
                return throws
            # Restrict r axis range based off off UNTHROWN TOKENS.
            # WHY -3?
            max_r = min(5, -3 + (9 - self.unthrown_lowers))
            ran_r = range(-4, max_r)
        # Generate all positions where the given playe may throw a token
        available_tiles = [(r,q) for r in ran_r for q in ran_q if -r-q in ran_q]

        # Convert from tile positions to 3-tuple move as defined in specs
        # Note the token type is unspecified for efficiency, this way only one
        # throw list is created.
        throws = []
        for token in COUNTERS.keys():
            throws += [("THROW", token, rq) for rq in available_tiles]
        return throws

    def generate_slides(self, thrown_pieces):
        """
        Generate all slide moves for the movers thrown pieces.
        """
        slides = []
        for pos in chain.from_iterable(thrown_pieces.values()):
            slides += [("SLIDE", pos, adj_pos) for adj_pos in self.get_adjacents(pos)]
        return slides

    def generate_swings(self, thrown_pieces):
        """
        Generate all swing moves for the movers thrown pieces.
        """
        swings = []
        for p in chain.from_iterable(thrown_pieces.values()):
            for q in chain.from_iterable(thrown_pieces.values()):
                adj_q = self.get_adjacents(q)
                if p in adj_q:
                    adj_q.remove(p)
                    swing_moves = list(set(adj_q) - set(self.get_adjacents(p)))
                    swings += [("SWING", p, s) for s in swing_moves]
        return swings

    def get_adjacents(self,position):
        """
        Get all adjacent tiles to the input position.
        """
        r,q = position
        ran = range(-4,5)
        return [(r+i, q+j) for i in [-1,0,1] for j in [-1,0,1]
                if i != j and r+i in ran and q+j in ran and -(r+i)-(q+j) in ran]
