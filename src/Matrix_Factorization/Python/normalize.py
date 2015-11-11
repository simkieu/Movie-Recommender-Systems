from numpy import *


def normalize(A, m):
    M = tile(m, (A.shape[0],1))
    R = A - M
    return R