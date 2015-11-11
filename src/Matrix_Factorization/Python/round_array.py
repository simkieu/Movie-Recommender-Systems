from round_to_half import *
from copy import *


def round_array(B):
    A = copy(B)
    for i in range(len(B)):
        A[i] = round_to_half(B[i])
    return A