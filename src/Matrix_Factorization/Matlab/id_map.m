function [u,v] = id_map(tr)
    u = zeros(1,730);
    v = zeros(1,6373);
    user = tr(:,1);
    movie = tr(:,2);
    user = sort(user);
    movie = sort(movie);
    u(1) = user(1);
    v(1) = movie(1);
    c1 = 2;
    for i=1:99999
        if user(i)~=user(i+1)
            u(c1) = user(i+1);
            c1 = c1 + 1;
        end
    end
    c2 = 2;
    for i=1:99999
        if movie(i)~=movie(i+1)
            v(c2) = movie(i+1);
            c2 = c2 + 1;
        end
    end
end