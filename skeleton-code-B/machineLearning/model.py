import numpy as np
from scipy.optimize import fmin_cg


board_data = np.genfromtxt("board_data.csv", dtype = str, delimiter = ",")

game_data = board_data[np.where(board_data[:, 0] == "OPENING")][:, 1:].astype(float)


def f(x, s, t):
    return 1/2*np.sum((t - s.dot(x))**2)

def fprime(x, s, t):
    return  (s.dot(x) - t).dot(s)


features = midgame_data[:,:-1]
tvs = midgame_data[:,-1]
x0 = [0.2, 0.15, 0.1, 0.05, 0.05]

res = fmin_cg(f, x0, fprime, (features, tvs))
print(res)
