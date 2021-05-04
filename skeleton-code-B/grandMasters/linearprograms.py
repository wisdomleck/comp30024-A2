"""
Solver for single-stage, zero-sum matrix-form games using scipy default
linear programming routines.

Original by Matthew Farrugia-Roberts, 2021

Students
* please note this implementation is not guaranteed to be free of errors,
  for example it has not been extensively tested.
* please report bugs to <matt.farrugia@unimelb.edu.au>.
* please feel free adapt for your own use-case.
"""

import numpy as np
import scipy.optimize as opt

def get_alpha(O, P, m, n):
    P = np.delete(P, m, axis = 0)
    O = np.delete(O, n, axis = 1)

    e = P[:, n].flatten()
    f = O[m, :-1].flatten()

    P = np.delete(P,  n, axis = 1)
    O = np.delete(O, m, axis = 0)

    print("O:", O)
    print("P:", P)
    print("f:", f)
    print("e:", e)

    #Solve linear program
    res = opt.linprog(
        c= -e, A_ub= -P.T, b_ub= -f,
        A_eq = np.ones((1,len(e))),
        b_eq = [1], bounds = (0, 1),
    )

    """print(res.success)
    print(res.x)"""

    if res.success:
        print(res.x)
        return -res.fun
    return -2

def get_beta(O, P, m, n):
    P = np.delete(P, a, axis = 0)
    O = np.delete(O, b, axis = 1)

    f = P[:-1, n].flatten()
    e = O[m, :].flatten()

    P = np.delete(P,  n, axis = 1)
    O = np.delete(O, m, axis = 0)

    print("O:", O)
    print("P:", P)
    print("f:", f)
    print("e:", e)

    res = opt.linprog(
        c = e, A_ub = O, b_ub = f,
        A_eq = np.ones((1, len(e))),
        b_eq = [1], bounds = (0, 1)
    )

    """
    A_ub = O, b_ub = f,
    """
    """print(res.success)
    print(res.x)"""

    if res.success:
        print(res.x)
        return res.fun
    return 2

def solve_game(V, maximiser=True, rowplayer=True):
    """
    Given a utility matrix V for a zero-sum game, compute a mixed-strategy
    security strategy/Nash equilibrium solution along with the bound on the
    expected value of the game to the player.
    By default, assume the player is the MAXIMISER and chooses the ROW of V,
    and the opponent is the MINIMISER choosing the COLUMN. Use the flags to
    change this behaviour.

    Parameters
    ----------
    * V: (n, m)-array or array-like; utility/payoff matrix;
    * maximiser: bool (default True); compute strategy for the maximiser.
        Set False to play as the minimiser.
    * rowplayer: bool (default True); compute strategy for the row-chooser.
        Set False to play as the column-chooser.

    Returns
    -------
    * s: (n,)-array; probability vector; an equilibrium mixed strategy over
        the rows (or columns) ensuring expected value v.
    * v: float; mixed security level / guaranteed minimum (or maximum)
        expected value of the equilibrium mixed strategy.

    Exceptions
    ----------
    * OptimisationError: If the optimisation reports failure. The message
        from the optimiser will accompany this exception.
    """
    V = np.asarray(V)
    # lprog will solve for the column-maximiser
    if rowplayer:
        V = V.T
    if not maximiser:
        V = -V
    m, n = V.shape
    # ensure positive

    c = -V.min() + 1
    Vpos = V + c

    # solve linear program
    res = opt.linprog(
        np.ones(n),
        A_ub=-Vpos,
        b_ub=-np.ones(m),
    )
    if res.status:
        raise OptimisationError(res.message) # TODO: propagate whole result
    # compute strategy and value

    v = 1 / res.x.sum()

    s = res.x * v
    v = v - c # re-scale
    if not maximiser:
        v = -v
    return s, v


class OptimisationError(Exception):
    """For if the optimiser reports failure."""


if __name__ == "__main__":
    # Rock paper scissors example (row player, maximiser)
    print("test: rock paper scissors")
    RPS = np.array([
        [  0, -1, +1 ],
        [ +1,  0, -1 ],
        [ -1, +1,  0 ],
    ])
    print("game:", *RPS, sep="\n ")
    print("soln:", *solve_game(RPS))
    print("true:", np.array([1/3, 1/3, 1/3]), 0.0)
    print()
    """
    print("test: textbook example")
    # Hespanha textbook example (column player, minimiser)
    A = np.array([
        [  3,  0 ],
        [ -1,  1 ],
    ])
    print("game:", A, sep="\n")
    print("soln:", *solve_game(A, maximiser=False, rowplayer=False))
    print("true:", np.array([1/5, 4/5]), 3/5)
    print()

    print("test: student example")
    V = np.array([[3, -1], [-1, -1]])
    print("game:", V, sep="\n")
    print("soln:", *solve_game(V, maximiser=True))
    print("true:", "(any strategy)         ", -1.0)
    print()"""

    O = np.ones(shape = (10, 10))
    P = -O

    O = np.append(O, np.full((O.shape[0], 1), 2), axis = 1)
    P = np.append(P, np.full((1, P.shape[1]), -2), axis = 0)

    """P[3,:] = 0.2
    P[:,7] = 0.1
    P[2,2] = 0.1
    P[9,3:6] = 0.3

    O[0,1:6] = -0.3
    O[8,8] = -0.3
    O[:, 5] = -0.3"""

    a = 4
    b = 3
    alpha_ab = get_alpha(O, P, a, b)
    beta_ab = get_beta(O, P, a, b)
    print(alpha_ab, beta_ab)
