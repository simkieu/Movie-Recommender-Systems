function a = round_to_half(b)
    d = b - floor(b);
    if d < 0.25
        a = floor(b);
    elseif d < 0.75
        a = (floor(b)+ceil(b))/2;
    else
        a = ceil(b);
    end
end