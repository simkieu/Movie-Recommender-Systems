function M = fill_matrix(A)
%     M = A;
%     for i=1:size(M,1)
%         a = M(i,:);
%         b = a(a>0);
%         m = mean(b);
%         if m==0
%             m = 2.5;
%         end
%         for j=1:size(M,2)
%             if M(i,j) == 0
%                 M(i,j) = m;
%             end
%         end
%     end

%Fill by mean of each column instead of row
    M = A;
    for i=1:size(M,2)
        a = M(:,i);
        b = a(a>0);
        if isempty(b)
            m = 3;
        else
            m = mean(b);
        end
        for j=1:size(M,1)
            if M(j,i) == 0
                M(j,i) = m;
            end
        end
    end
end