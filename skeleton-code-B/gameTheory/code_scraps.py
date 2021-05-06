def best_move(self):
    s, v, moves, d_rows = self.SM_solver(self.root, -2, 2, 0)
    moves = moves[:, 0].delete(d_rows, axis = 0)
    bmi = random.choices(range(len(s)), weights = s, k = 1)[0]
    return moves[bmi].board.move[0]

def SM_solver(self, state, alpha, beta, depth):
    if state.is_terminal() or depth == self.cutoff:
        return None, state.eval(), None, None

    moves = state.generate_nodes()
    O, P = self.bound(moves, alpha, beta)
    d_rows = d_cols = []
    for m in range(len(moves)):
        for n in range(len(moves[m])):
            if m not in d_rows and n not in d_cols:
                m -= len(d_rows)
                n -= len(d_cols)
                a = get_alpha(O, P, m, n)
                b = get_beta(O, P, m, n)
                q = moves[m,n]

                if a >= b:
                    _, v, _, _ = self.SM_solver(q, a, a + 0.01, depth + 1)
                    if v <= a:
                        d_rows.append(m)
                        O = np.delete(O, m, axis = 0)
                        P = np.delete(P, m, axis = 0)

                    else:
                        d_cols.append(n)
                        O = np.delete(O, n, axis = 1)
                        P = np.delete(P, n, axis = 1)

                else:
                    _, v, _, _ = self.SM_solver(q, a, b, depth + 1)
                    if v <= a:
                        d_rows.append(m)
                        O = np.delete(O, m, axis = 0)
                        P = np.delete(P, m, axis = 0)
                    elif v >= b:
                        d_cols.append(n)
                        O = np.delete(O, n, axis = 1)
                        P = np.delete(P, n, axis = 1)
                    else:
                        O[m,n] = P[m,n] = v

    s, v = solve_game(P)
    return s, v, moves, d_rows

def bound(self, moves, alpha, beta):
    P = np.empty(moves.shape)
    O = np.empty(moves.shape)
    for m in range(moves.shape[0]):
        p = np.min([node.eval() - 0.05 for node in moves[m, :]])
        P[m,:] = np.full(P.shape[1], p)

    for n in range(moves.shape[1]):
        o = np.max([node.eval() + 0.05 for node in moves[:, n]])
        O[:, n] = np.full(P.shape[0], o)

    O = np.append(O, np.full((O.shape[0], 1), beta), axis = 1)
    P = np.append(P, np.full((1, P.shape[1]), alpha), axis = 0)
    return O, P
