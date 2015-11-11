from numpy import *
from copy import *


def train_test(B, pos, num_test):
    num_train = 100000 - num_test
    tt = copy(B[pos*num_test:(pos+1)*num_test, :])
    tr = zeros((num_train,3))
    index = 0
    for i in range(100000):
        if i<pos*num_test or i>(pos+1)*num_test-1:
            tr[index, :] = copy(B[i, :])
            index += 1
    return tr, tt