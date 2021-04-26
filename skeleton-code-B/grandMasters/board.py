from itertools import product, chain
from copy import deepcopy

COUNTERS = {'s':'p', 'p':'r', 'r':'s'}
COUNTERED = {'p':'s', 'r':'p', 's':'p'}
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

    def __str__(self):
        return f"Thrown Uppers: {self.thrown_uppers}\nThrown Lowers: {self.thrown_lowers}\nMove:{self.move}\n"

    def apply_turn(self, upper_move, lower_move):
        """
        Given an upper and lower move, create the resultant board from
        apply these moves to the current board.
        """

        # Create deepcopy of token related variables
        new_thrown_uppers = deepcopy(self.thrown_uppers)
        new_thrown_lowers = deepcopy(self.thrown_lowers)
        unthrown_uppers = self.unthrown_uppers
        unthrown_lowers = self.unthrown_lowers

        # In a slide or swing move, first remove piece from board before
        # re-adding it to its correct location
        if upper_move[0] != "THROW":
            t = self.remove_piece(upper_move[1], new_thrown_uppers)
            u_move = (t, upper_move[2])
        else:
            u_move = (upper_move[1], upper_move[2])
            unthrown_uppers -= 1

        if lower_move[0] != "THROW":
            t = self.remove_piece(lower_move[1], new_thrown_lowers)
            l_move = (t, lower_move[2])
        else:
            l_move = (lower_move[1], lower_move[2])
            unthrown_lowers -= 1

        # Update deepcopied thrown piece dictionaries and create new board object
        self.add_piece(u_move, new_thrown_uppers, new_thrown_lowers)
        self.add_piece(l_move, new_thrown_lowers, new_thrown_uppers)
        return Board(new_thrown_uppers, new_thrown_lowers, unthrown_uppers, unthrown_lowers, self.turn+1, (upper_move, lower_move))

    """ Same as apply_turn, but for one player. Used for MCTS """
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
            if upper_move[0] != "THROW":
                t = self.remove_piece(move[1], new_thrown_uppers)
                u_move = (t, move[2])
            else:
                u_move = (move[1], move[2])
                unthrown_uppers -= 1

        self.add_piece(u_move, new_thrown_uppers, new_thrown_lowers)

            return Board(new_thrown_uppers, new_thrown_lowers, unthrown_uppers, unthrown_lowers, self.turn+1, (upper_move, lower_move))

        else if player == "LOWER":

            if lower_move[0] != "THROW":
                t = self.remove_piece(lower_move[1], new_thrown_lowers)
                l_move = (t, lower_move[2])
            else:
                l_move = (lower_move[1], lower_move[2])
                unthrown_lowers -= 1

            self.add_piece(l_move, new_thrown_lowers, new_thrown_uppers)

            return Board(new_thrown_uppers, new_thrown_lowers, unthrown_uppers, unthrown_lowers, self.turn+1, (upper_move, lower_move))


    def add_piece(self, piece, mover_dict, other_dict):
        """
        Piece is a tuple with containing the piece's token type and position.
        This function adds such a token to the required position, removing any
        token that is destroyed as a result.
        """

        # Get type of token which counters and is countered by added token.
        token, pos = piece
        token_g = COUNTERS[token]
        token_b = COUNTERED[token]

        # If counter token at the position, do nothing.
        if pos in mover_dict[token_b] or pos in other_dict[token_b]:
             return

        # Remove any instance of countered tokens from the position and add
        # new token to position.
        mover_dict[token_g] = [p for p in mover_dict[token_g] if p != pos]
        other_dict[token_g] = [p for p in other_dict[token_g] if p != pos]
        mover_dict[token].append(pos)

    def remove_piece(self, pos, mover_dict):
        """
        Remove token exisiting on input position from the movers thrown dictionary.
        Return the token type.
        """

        for key,value in mover_dict.items():
            if pos in value:
                value.remove(pos)
                return key


    # Assumes the turn is valid but checks
    def check_turn(self, upper_move, lower_move):
        return

    """ The moves passed into the sequential version of MCTS """
    def generate_seq_turn(self):
        lower_moves = {"THROWS": [], "SLIDES": [], "SWINGS": []}
        upper_moves = {"THROWS": [], "SLIDES": [], "SWINGS": []}

        lower_moves["THROWS"] = self.generate_throws("LOWER")
        lower_moves["SLIDES"] = self.generate_slides(self.thrown_lowers)
        lower_moves["SWINGS"] = self.generate_swings(self.thrown_lowers)

        upper_moves["THROWS"] = self.generate_throws("UPPER")
        upper_moves["SLIDES"] = self.generate_slides(self.thrown_uppers)
        upper_moves["SWINGS"] = self.generate_swings(self.thrown_uppers)

        return {"UPPER": upper_moves, "LOWER":, lower_moves}


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

        return list(product(upper_moves, lower_moves))

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
            # Restrict r axis range based off turn.
            min_r = max(-4, 4 - self.turn)
            ran_r = range(min_r, 5)

        else:
            # Return empty list if throws are exhausted.
            if self.unthrown_lowers == 0:
                return throws
            # Restrict r axis range based off turn.
            max_r = min(5, -3 + self.turn)
            ran_r = range(-4, max_r)
        # Generate all positions where the given playe may throw a token
        available_tiles = [(r,q) for r in ran_r for q in ran_q if -r-q in ran_q]

        # Convert from tile positions to 3-tuple move as defined in specs
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
