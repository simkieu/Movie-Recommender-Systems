from numpy import *


def build_matrix(tr, u, v, num_test, no_user, no_movie):
    num_train = 100000 - num_test
    M = zeros((no_user, no_movie))
    for i in range(num_train):
        user_id = tr[i, 0]
        movie_id = tr[i, 1]
        row_index = u[user_id]
        col_index = v[movie_id]
        M[row_index, col_index] = tr[i, 2]
    return M