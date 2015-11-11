function count = num_user(A)
    B = A(:,1);
    count = 1;
    for i=1:99999
        if B(i) ~= B(i+1)
            count = count+1;
        end
    end
end