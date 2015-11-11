function A = trim_rating(B)
    A = B;
    for i=1:length(B)
        if A(i) < 1
            A(i) = 1;
        end
        if A(i) > 5
            A(i) = 5;
        end
    end
end