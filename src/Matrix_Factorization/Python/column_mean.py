from numpy import *


def column_mean(A):
    m = zeros((1, A.shape[1]))
    for i in range(A.shape[1]):
        m[0, i] = mean(A[:, i])
    return m

