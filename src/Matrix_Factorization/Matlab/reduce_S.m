function Sk = reduce_S(S,k)
    Sk = zeros(k);
    for i = 1:k
        Sk(i,i) = S(i,i);
    end
end