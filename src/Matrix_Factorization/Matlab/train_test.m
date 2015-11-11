function [tr, tt] = train_test(B,pos,num_test)
    num_train = 100000 - num_test;
    tt = B((pos-1)*num_test+1:pos*num_test,:);
    tr = zeros(num_train,3);
    index = 1;
    for i =1:100000
        if i<(pos-1)*num_test+1 || i>pos*num_test
            tr(index,:) = B(i,:);
            index = index+1;
        end
    end
end