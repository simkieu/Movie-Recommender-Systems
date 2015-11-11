from numpy import *

def S_to_matrix(Ss):
    length = len(Ss)
    Sk = zeros((length, length))
    for i in range(length):
        Sk[i, i] = Ss[i]
    return Sk
