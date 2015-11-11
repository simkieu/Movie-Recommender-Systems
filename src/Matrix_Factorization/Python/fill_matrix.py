from copy import *
from numpy import *


def fill_matrix(A):
    M = copy(A)
    for i in range(M.shape[1]):
        a = M[:, i]
        b = a[a>0]
        if sum(b) == 0:
            m = 3
        else:
            m = mean(b)
        for j in range(M.shape[0]):
            if M[j, i] == 0:
                M[j, i] = m
    return M

