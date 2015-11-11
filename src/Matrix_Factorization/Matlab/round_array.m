function A = round_array(B)
    A = B;
    for i = 1:length(B)
        A(i) = round_to_half(B(i));
    end
end