from copy import *


def id_map(B):
    user = copy(B[:, 0])
    movie = copy(B[:, 1])
    user.sort()
    movie.sort()
    u = {user[0]: 0}
    v = {movie[0]: 0}

    c1 = 1
    for user_id in user:
        if user_id not in u:
            u.update({user_id: c1})
            c1 += 1

    c2 = 1
    for movie_id in movie:
        if movie_id not in v:
            v.update({movie_id: c2})
            c2 += 1

    return u, v