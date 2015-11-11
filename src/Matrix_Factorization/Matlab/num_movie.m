function count = num_movie(A)
    B = A(:,2);
    B = sort(B);
    count = 1;
    for i=1:99999
        if B(i) ~= B(i+1)
            count = count+1;
        end
    end
end