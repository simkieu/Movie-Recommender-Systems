% load('results-not rounded.mat')
% rmse1 = rmse;
% load('results_rounded.mat')
% rmse2 = rmse;
rmse3 = load('_rmse.csv');
%rmse4 = load('rmse-user-pearson.csv');

% a1 = mean(rmse1,1);
% a2 = mean(rmse2,1);

% a1 = rmse1(8,:);
% a2 = rmse2(8,:);

% a1 = rmse1(:,1);
% a2 = rmse1(:,30);
%a3 = rmse4(:,2);

%a4 = mean(rmse4,1);
%a1 = rmse3(8,:);
a1 = rmse3(:,12);
a2 = rmse3(:,11);

%b = 1:30;
b = 3:10;

hold on
plot(b,a1,'LineWidth',1)
plot(b,a2,'r','LineWidth',1)
% plot(b,a3,'g','LineWidth',3)
%title('RMSE of with k=12, k=1, and with the Pearson method','fontweight','bold','fontsize',12)
%title('RMSE of with the best number of CV-folds over different k-dimensions','fontweight','bold','fontsize',12)
title('RMSE of with the best k-dimensions over different number of folds','fontweight','bold','fontsize',12)
%title('Average RMSE of different folds on different k-dimensions','fontweight','bold','fontsize',12)
%title('RMSE of non-rounded with k=1 and k=30','fontweight','bold','fontsize',12)
%title('Average RMSE of different k-dimensions on different number of folds','fontweight','bold','fontsize',12)
xlabel('k-dimension','fontweight','bold','fontsize',12);
%xlabel('Number of folds','fontweight','bold','fontsize',12);
ylabel('RMSE','fontweight','bold','fontsize',12);
%legend('Not rounded ratings','Rounded ratings')
%legend('k = 12','k = 1','Pearson-User')
legend('k = 12','k = 11')
hold off
