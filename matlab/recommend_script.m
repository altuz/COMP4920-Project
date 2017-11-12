% Load data from specific test folder
tic % for timing
load ../control_test/500/combined_rating % Loads R and R_train
% Actual ratings
% R = 'read from file'

% Training set
% R_train = 'read from file'

% Mean of training set
r_bar = mean(R_train(:),'omitnan');

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
b = pinv(A' * A + lambda * eye(n_A, m_A))*(A' * c); % with regularisation
% b = pinv(A' * A)*(A' * c); % no regularisation
b_u = b(1:n,1);
b_i = b((n+1):(n+m),1);

% Compute R_hat
R_hat = zeros(n,m);

for j = 1:m
    for i = 1:n 
		if ~isnan(R(i,j)) % Don't really need this if statement
			predictR = r_bar + b_u(i) + b_i(j);

			% Range for 'ratings' is 0 to 1
			if predictR > 1
				predictR = 1;
			elseif predictR < 0
				predictR = 0;
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

			if predictR > 1
				predictR = 1;
			elseif predictR < 0
				predictR = 0;
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
[U, sigma, vt, flag] = svds(r_demeaned, 100);

% Making predictions from decomposed matrix
r_tilde_latent = U * sigma * vt';
r_hat_latent = r_tilde_latent + r_bar_mat;

% Calculate RMSE
diff_train_latent = R_train - r_hat_latent;
RMSE_train_latent = sqrt(mean((diff_train_latent(:)).^2,'omitnan'));

diff_test_latent = R - r_hat_latent;
RMSE_test_latent = sqrt(mean((diff_test_latent(:)).^2,'omitnan'));
fprintf("Script complete\n")
toc