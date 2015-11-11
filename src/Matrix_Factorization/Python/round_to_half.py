from numpy import *


def round_to_half(b):
    d = b - floor(b)
    if d < 0.25:
        a = floor(b)
    elif d < 0.75:
        a = (floor(b)+ceil(b))/2
    else:
        a = ceil(b)
    return a