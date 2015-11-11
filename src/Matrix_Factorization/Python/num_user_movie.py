from copy import *


def num_user(A):
    b = A[:, 0]
    count = 1
    for i in range(99999):
        if b[i] != b[i+1]:
            count += 1
    return count


def num_movie(A):
    b = copy(A[:, 1])
    b.sort()
    count = 1
    for i in range(99999):
        if b[i] != b[i+1]:
            count += 1
    return count
    pass