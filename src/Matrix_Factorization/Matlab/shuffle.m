function B = shuffle(A)
    B = zeros(size(A));
    r = randperm(100000);
    for i = 1:100000
        B(i,:) = A(r(i),:);
    end
end