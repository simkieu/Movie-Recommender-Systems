from num_user_movie import *
from shuffle import *
from train_test import *
from id_map import *
from build_matrix import *
from fill_matrix import *
from column_mean import *
from normalize import *
from numpy.linalg import svd
from S_to_matrix import *
from trim_rating import *
from predict_ratings import *
from round_array import *
from os.path import *
from create_file import *


class SVD:
    def __init__(self):
        pass

    def main(self):

        # Read data
        print('Reading data...\n')
        filename1 = '_data.csv'
        filename2 = 'ratings.dat'
        if not exists(filename1):
            if not exists(filename2):
                print('Error: Please add file', filename2, 'into the path!')
                exit(1)
            else:
                create_file(filename2, filename1)
        A = loadtxt(filename1, delimiter=',')

        # Initialize variables
        no_user = num_user(A)
        no_movie = num_movie(A)
        B = shuffle(A)

        # Set parameters
        k_set = [1, 3]
        fold_set = [3, 4]
        rmse = zeros((len(fold_set), len(k_set)))
        ratings_round = False

        # Main algorithm
        for ff in range(len(fold_set)):
            num_fold = fold_set[ff]
            print(str(num_fold) + '-fold Cross Validation begins.\n')
            num_test = int(floor(100000/num_fold))
            num_train = 100000 - num_test

            for kk in range(len(k_set)):
                k = k_set[kk]
                print('Reducing dimensions to', k, '.')
                error_each_fold = zeros((num_fold,1))

                for i in range(num_fold):
                    print('Fold ' + str(i+1) + '. Splitting train/test...')
                    tr, tt = train_test(B, i, num_test)
                    u, v = id_map(B)

                    # Build matrix R in the paper
                    print('Building matrix R...')
                    R_raw = build_matrix(tr, u, v, num_test, no_user, no_movie)
                    R_filled = fill_matrix(R_raw)
                    m = column_mean(R_filled)
                    R = normalize(R_filled, m)

                    # Dimensionality Reduction
                    print('Dimensionality Reduction...')
                    U, S, V = svd(R, full_matrices=False)
                    Ss = copy(S[0:k])
                    Sk = S_to_matrix(Ss)
                    Uk = copy(U[:, 0:k])
                    Vk = copy(V[0:k, :])
                    sqrt_Sk = sqrt(Sk)
                    US = dot(Uk,transpose(sqrt_Sk))
                    SV = dot(sqrt_Sk, Vk)

                    # Predict the ratings
                    print('Predicting ratings...')
                    pr = predict_ratings(US, SV, m, u, v, tt, num_test)
                    if ratings_round == True:
                        pr = round_array(pr)
                    pr_trim = trim_rating(pr)

                    # Find error
                    print('Calculating error...')
                    real = copy(tt[:, 2])
                    error = pr_trim - real
                    error_each_fold[i] = sqrt(sum(error**2)/num_test)
                    print('End one fold.\n')

                rmse[ff, kk] = mean(error_each_fold)

        savetxt("_rmse.csv", rmse, fmt='%.4f', delimiter=",")
        print(rmse)



S = SVD()
S.main()