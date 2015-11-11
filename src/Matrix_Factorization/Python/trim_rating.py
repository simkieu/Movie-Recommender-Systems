from copy import *


def trim_rating(B):
    A = copy(B)
    for i in range(len(B)):
        if A[i] < 0.5:
            A[i] = 0.5
        if A[i] > 5:
            A[i] = 5
    return A