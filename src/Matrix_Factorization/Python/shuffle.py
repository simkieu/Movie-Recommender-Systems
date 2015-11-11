from numpy import *


def shuffle(A):
    B = zeros(A.shape)
    r = random.permutation(100000)
    for i in range(100000):
        B[i, :] = A[r[i], :]
    return B