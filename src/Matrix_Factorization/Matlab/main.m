clear
clc

%% Read data
A = load('_data.csv');
m = num_user(A);
n = num_movie(A);
B = shuffle(A); %Shuffle the data

%% Set parameters
k_set = [3 4 5]; %Set of k-dimension to reduce to
fold_set = [3 4]; %Number of folds: use this to train with different train/test ratio
rmse = zeros(length(fold_set),length(k_set)); %RMSE for each fold and dimension
ratings_round = 0; %0 is no round the predicted ratings, 1 is round it.


%% Main algorithm
for ff=1:length(fold_set) %For each different train/test ratios
    num_fold = fold_set(ff);
    num_test = floor(100000/num_fold);
    num_train = 100000 - num_test;
    for kk = 1:length(k_set) %For each k-dimensions
        k = k_set(kk);
        error_each_fold = zeros(num_fold,1);
        for i = 1:num_fold %Do num_fold-fold CV
            [tr, tt] = train_test(B,i,num_test);
            [u,v] = id_map(B);
            
            %Build matrix R in the paper
            R_raw = build_matrix(tr,u,v,num_test);
            R_filled = fill_matrix(R_raw); %I fill it using average of column instead of row like we did last afternoon since that's what the paper said.
            %m = mean(mean(R_filled))*ones(1,size(R_filled,2));
            m = mean(R_filled); %I tried different methods to calculate C_bar, this seems work best
            R = normalize(R_filled,m);
            
            %Dimensionality Reduction
            [U,S,V] = svd(R,'econ');
            Sk = reduce_S(S,k);
            Uk = U(:,1:k);
            Vk = V(:,end-k+1:end);
            sqrt_Sk = sqrt(Sk);
            US = Uk*sqrt_Sk';
            SV = sqrt_Sk*Vk';
            
            %Predict the ratings
            real = tt(:,3);
            pr = zeros(num_test,1);
            for j=1:num_test
                user_id = tt(j,1);
                movie_id = tt(j,2);
                r = u==user_id;
                c = v==movie_id;
                pr(j) = US(r,:)*SV(:,c)+m(c);
            end
            if ratings_round == 1
                pr = round_array(pr); %Rounded predicted ratings
            end
            pr_trim = trim_rating(pr); %Final predicted ratings
            
            %Find error
            error = pr_trim - real;
            error_each_fold(i) = sqrt(sum(error.^2)/num_test);
        end
        rmse(ff,kk) = mean(error_each_fold); %Output the RMSE for each k (k is the dimension reduced to)
    end
end
