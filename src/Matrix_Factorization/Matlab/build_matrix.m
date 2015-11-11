function M = build_matrix(tr,u,v,num_test)
    num_train = 100000 - num_test;
    M = zeros(730,6373);
    for i = 1:num_train
        user_id = tr(i,1);
        movie_id = tr(i,2);
        row_index = u==user_id;
        col_index = v==movie_id;
        M(row_index,col_index) = tr(i,3);
    end
end