from itertools import product, chain
import numpy as np

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
        return self.thrown_uppers == other.thrown_uppers and self.thrown_lowers == other.thrown_lowers and\
        self.unthrown_uppers == other.unthrown_uppers and self.unthrown_lowers == other.unthrown_lowers

    def __str__(self):
        return f"Thrown Uppers: {self.thrown_uppers}\nUnthrown Uppers: {self.unthrown_uppers}\nThrown Lowers: {self.thrown_lowers}\nUnthrown Lowers: {self.unthrown_uppers}\nMove:{self.move}\n"

    def player_pieces(self, player):
        if player == "UPPER":
            return self.thrown_uppers, self.unthrown_uppers
        else:
            return self.thrown_lowers, self.unthrown_lowers

    def opponent_pieces(self, player):
        if player == "UPPER":
            return self.player_pieces("LOWER")
        else:
            return self.player_pieces("UPPER")

    def is_win(self, player):
        other = "LOWER" if player == "UPPER" else "UPPER"

        return self.remaining_tokens(player) and not self.remaining_tokens(other) or\
        self.has_invincible(player) and\
        not self.has_invincible(other) and\
        self.remaining_tokens(other) == 1

    def is_draw(self):
        return (not self.remaining_tokens("UPPER") and not self.remaining_tokens("LOWER")) or\
        self.has_invincible("UPPER") and self.has_invincible("LOWER") or self.turn >= 30

    def chain(self, dict):
        return list(chain.from_iterable(dict.values()))

    def remaining_tokens(self, player):
        if player == "UPPER":
            return len(self.chain(self.thrown_uppers)) + self.unthrown_uppers
        else:
            return len(self.chain(self.thrown_lowers)) + self.unthrown_lowers

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

    def copy_dict(self, player_dict):
        new_dict = {}
        for key, value in player_dict.items():
            new_dict[key] = value.copy()
        return new_dict

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
    def apply_turn(self, upper_move, lower_move):
        # Create deepcopy of token related variables
        new_thrown_uppers = self.copy_dict(self.thrown_uppers)
        new_thrown_lowers = self.copy_dict(self.thrown_lowers)
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

    #def swap_players(self)
    def best_throw(self, player, pos):
        if player == "UPPER":
            player_thrown = self.thrown_uppers
            opponent_thrown = self.thrown_lowers
        else:
            player_thrown = self.thrown_lowers
            opponent_thrown = self.thrown_uppers

        ally_occupant = [key for key, value in player_thrown.items() if pos in value]
        opp_occupant = [key for key, value in opponent_thrown.items() if pos in value]

        bad_throws = []
        if ally_occupant:
            bad_throws.append(COUNTERS[ally_occupant[0]])
            bad_throws.append(COUNTERED[ally_occupant[0]])
        if opp_occupant:
            bad_throws.append(COUNTERS[opp_occupant[0]])

        good_throws = [t for t in "rps" if t not in bad_throws]

        max_opp_token = -1
        best_throw = None
        for throw in good_throws:
            if pos in opponent_thrown[COUNTERS[throw]]:
                return throw

            ps = len(opponent_thrown[COUNTERS[throw]])
            if ps > max_opp_token:
                max_opp_token = ps
                best_throw = throw

        return best_throw


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
        return [("THROW", self.best_throw(player, rq), rq) for rq in available_tiles]

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
