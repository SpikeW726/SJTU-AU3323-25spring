import numpy as np

WEIGHT1 = [[4**6, 4**5, 4**3, 4**2],[4**5, 4**4, 4**3, 4**2],[4**4, 4**3, 4**2, 4**1],[4**3, 4**2, 4**1, 4**0]]

def exp_heuristic(state):
    return np.sum([[WEIGHT1[i][j] * state[i][j] for j in range(4)] for i in range(4)] )

