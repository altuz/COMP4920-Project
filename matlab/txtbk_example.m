% Good site
% https://blogs.mathworks.com/loren/2015/04/22/the-netflix-prize-and-production-machine-learning-systems-an-insider-look/

% Lecturer/author of networked life txtbk coursera explanation vid
% https://www.youtube.com/watch?v=dGM4bNQcVKI

% Array filling optimizations
% https://au.mathworks.com/matlabcentral/answers/82989-fastest-way-to-fill-in-an-array

% Least squares solving
% https://au.mathworks.com/help/matlab/ref/mldivide.html

% Actual ratings
R = [5 4 4 NaN 5;
NaN 3 5 3 4;
5 2 NaN 2 3;
NaN 2 3 1 2;
4 NaN 5 4 5;
5 3 NaN 3 5;
3 2 3 2 NaN;
5 3 4 NaN 5;
4 2 5 4 NaN;
5 NaN 5 3 4]

% Training set
R_train = [5 4 4 NaN NaN;
NaN 3 5 NaN 4;
5 2 NaN NaN 3;
NaN NaN 3 1 2;
4 NaN NaN 4 5;
NaN 3 NaN 3 5;
3 NaN 3 2 NaN;
5 NaN 4 NaN 5;
NaN 2 5 4 NaN;
NaN NaN 5 3 4]

% Mean of training set
r_bar = mean(R_train(:),'omitnan');
% r_bar = 115/30 % for some reason txtbk example uses r_bar = 3.83

% Making matrix A for training set
[n, m] = size(R_train);
n_ratings = sum(~isnan(R_train(:))); 

A = zeros(n_ratings, n+m); % pre-fill for optimisation
c = zeros(n_ratings, 1); % pre-fill for optimisation

rowA = 1; 
for j = 1:m 
	for i = 1:n
		if ~isnan(R_train(i,j))
			A(rowA,i) = 1;
			A(rowA,n+j) = 1;
			% note: r = R_train(i,j)
			% fprintf('%d\n', R_train(i,j))

			c(rowA) = R_train(i,j) - r_bar; 
			
			rowA = rowA + 1;
		end
	end
end 

% Linear equation to solve
% (A' * A) * b = A' c
% b = (A' * A) \ (A' * c) % Don't use this, 
lambda = 1; % Is this how to regularise (A' * A) * b - lambda * b= A' c
[n_A, m_A] = size(A' * A);
%b = pinv(A' * A + lambda * eye(n_A, m_A))*(A' * c); % with regularisation
b = pinv(A' * A)*(A' * c); % no regularisation
b_u = b(1:n,1);
b_i = b((n+1):(n+m),1);

% Compute R_hat
R_hat = zeros(n,m);

for j = 1:m
    for i = 1:n 
		if ~isnan(R(i,j)) % Don't really need this if statement
			predictR = r_bar + b_u(i) + b_i(j);

			% Range for 'ratings' is 0 to 1
			if predictR > 5
				predictR = 5;
			elseif predictR < 1
				predictR = 1;
			end

			R_hat(i,j) = predictR;
		else
			R_hat(i,j) = NaN;
		end
	end
end

% Check the RMSE compared to training set
diff_train = R_train - R_hat;  
RMSE_train = sqrt(mean((diff_train(:)).^2,'omitnan')); 

diff_test = R - R_hat;  
RMSE_test = sqrt(mean((diff_test(:)).^2,'omitnan')); 

% movie similarity matrix
R_tilde = R_train - R_hat;
D_movie = zeros(m,m);

for j = 1:m
    for i = 1:m
		if ~(i == j)
			% Compute similarity value
			sum_i_sq = 0;
			sum_j_sq = 0;
			sum_pair = 0;
			for k = 1:n
				if ~isnan(R_tilde(k,i)) && ~isnan(R_tilde(k,j))
					sum_pair = sum_pair + R_tilde(k,i) * R_tilde(k,j);
					sum_i_sq = sum_i_sq + R_tilde(k,i) ^ 2;
					sum_j_sq = sum_j_sq + R_tilde(k,j) ^ 2;
				end
			end
			D_movie(i,j) = sum_pair/sqrt(sum_i_sq*sum_j_sq);
		else 
			D_movie(i,j) = NaN;
		end
	end
end

% r_hat_n for neighborhood model
R_hat_n = zeros(n,m);
L = 2; % Variable for number of neighbors that will count in neighborhood model
for j = 1:m 
	for i = 1:n
		if ~isnan(R(i,j)) % Don't really need this if statement, unless we're testing for RMSE 

			% Sum for top 2 movie neighbors to movie j 
			neigh_abs = [(1:m)', abs(D_movie(:,j))]; % Store movie neighbors to j and the movie index
			neigh_abs = sortrows(neigh_abs, 2, 'descend'); 
			neigh_abs = neigh_abs(sum(isnan(neigh_abs),2)==0);

			% TODO Calculate neighborhood factor
			% Step 1: Find top L
			sum_dr = 0; % using similarity d as the prediction weight (basic method)
			sum_abs_d = 0;
			for index = 1:min(length(neigh_abs), L) % For neighbor movies, L is limit variable
				n_i = neigh_abs(index);
                % fprintf('n_i:%d\n', n_i)
				if ~isnan(R_tilde(i, n_i))
					% Using similarity d as the weighting
                    
					% fprintf('user: %d, neighbor: %d\n', i, n_i)
					% fprintf('cosine coeff: %d\n', D_movie(j,n_i))
					sum_dr = sum_dr + D_movie(j,n_i) * R_tilde(i,n_i);
					sum_abs_d = sum_abs_d + abs(D_movie(j,n_i));
				end
			end

			% Neighborhood model: Calc normalised weighted sum of weightings 
			if (sum_abs_d == 0) 
				sum_d = 0;
			else
				sum_d = sum_dr/sum_abs_d;
			end

			predictR = r_bar + b_u(i) + b_i(j) + sum_d;

			if predictR > 5
				predictR = 5;
			elseif predictR < 1
				predictR = 1;
			end

			R_hat_n(i,j) = predictR;
		else
			R_hat_n(i,j) = NaN;
		end
	end
end

% TODO play around with capping in above if predictR > 5 statement
% Check the RMSE compared to training set
diff_train_n = R_train - R_hat_n;
RMSE_train_n = sqrt(mean((diff_train_n(:)).^2,'omitnan')); 

diff_test_n = R - R_hat_n;  
RMSE_test_n = sqrt(mean((diff_test_n(:)).^2,'omitnan'));

% Start of Latent Fagtor
% TODO: Might want to consider R_tilde/R_hat instead of R?
r_bar_mat = repmat(r_bar, size(R_train));
r_demeaned = R_train - r_bar_mat;
r_demeaned(isnan(r_demeaned))=0;
[U, sigma, vt, flag] = svds(r_demeaned, 5);

% Making predictions from decomposed matrix
r_tilde_latent = U * sigma * vt';
r_hat_latent = r_tilde_latent + r_bar_mat;

% Calculate RMSE
diff_train_latent = R_train - r_hat_latent;
RMSE_train_latent = sqrt(mean((diff_train_latent(:)).^2,'omitnan'));

diff_test_latent = R - r_hat_latent;
RMSE_test_latent = sqrt(mean((diff_test_latent(:)).^2,'omitnan'));
fprintf("Script complete\n")

% Combining latent factor and neighborhood model
% Making matrix A for training set
[n, m] = size(R_train);
n_ratings = sum(~isnan(R_train(:))); 

A = zeros(n_ratings, 2); % pre-fill for optimisation
c = zeros(n_ratings, 1); % pre-fill for optimisation

rowA = 1; 
for j = 1:m 
	for i = 1:n
		if ~isnan(R(i,j))
			A(rowA,1) = R_hat_n(i,j); % Column 1 for neighborhood
			A(rowA,2) = r_hat_latent(i,j); % Column 2 for latent factor 

			c(rowA) = R(i,j); 
			
			rowA = rowA + 1;
		end
	end
end 

% Linear equation to solve
% (A' * A) * b = A' c
% b = (A' * A) \ (A' * c) % Don't use this, 
lambda = 1; % Is this how to regularise (A' * A) * b - lambda * b= A' c
[n_A, m_A] = size(A' * A);
% w = pinv(A' * A + lambda * eye(n_A, m_A))*(A' * c); % with regularisation
w = pinv(A' * A)*(A' * c); % no regularisation 

% Compute R_hat for combined model
R_hat_c = zeros(n,m);

for j = 1:m
    for i = 1:n 
		if ~isnan(R(i,j)) % Don't really need this if statement
			predictR = w(1) * R_hat_n(i,j) + w(2) * r_hat_latent(i,j);

			% Range for 'ratings' is 0 to 1
			if predictR > 5
				predictR = 5;
			elseif predictR < 1
				predictR = 1;
			end

			R_hat_c(i,j) = predictR;
		else
			R_hat_c(i,j) = NaN;
		end
	end
end

% Check the RMSE compared to training set
diff_train_c = R_train - R_hat_c;  
RMSE_train_c = sqrt(mean((diff_train_c(:)).^2,'omitnan')); 

diff_test_c = R - R_hat_c;  
RMSE_test_c = sqrt(mean((diff_test_c(:)).^2,'omitnan')); 

fprintf("----Baseline_predictor----\n");
fprintf("RMSE_train %f\n", RMSE_train);
fprintf("RMSE_test %f\n", RMSE_train);

fprintf("----Neighborhood----\n");
fprintf("RMSE_train_n %f\n", RMSE_train_n);
fprintf("RMSE_test_n %f\n", RMSE_test_n);

fprintf("----Latent factor----\n");
fprintf("RMSE_train_latent %f\n", RMSE_train_latent);
fprintf("RMSE_test_latent %f\n", RMSE_test_latent);

fprintf("----Combined----\n");
fprintf("RMSE_train_c %f\n", RMSE_train_c);
fprintf("RMSE_test_c %f\n", RMSE_test_c);
toc