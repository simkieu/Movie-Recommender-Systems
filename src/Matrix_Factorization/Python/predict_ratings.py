from numpy import *


def predict_ratings(US, SV, m, u, v, tt, num_test):
    pr = [0]*num_test
    for j in range(num_test):
        user_id = tt[j, 0]
        movie_id = tt[j, 1]
        r = u[user_id]
        c = v[movie_id]
        pr[j] = float("{0:.4f}".format(dot(US[r, :], SV[:, c]) + m[0, c]))
    return pr