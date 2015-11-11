function R = normalize(A,m)
    M = repmat(m,size(A,1),1);
    R = A - M;
end