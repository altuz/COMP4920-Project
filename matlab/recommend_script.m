% Load data from specific test folder
tic % for timing
load ../control_test/1000/combined_rating_med % Loads R and R_train
load ../control_test/ave_hours
% Actual ratings
% R = 'read from file'

% Training set
% R_train = 'read from file'
R_to_predict = R_train;
R_to_predict(isnan(R_to_predict)) = 0;
R_to_predict = R - R_to_predict;
R_to_predict(R_to_predict == 0) = NaN;

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

diff_test = R_to_predict - R_hat;  
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
%             elseif predictR < 0.2
%                 predictR = 0.2;
%             elseif predictR < 0.4
%                 predictR = 0.4;
%             elseif predictR < 0.6
%                 predictR = 0.6;
%             elseif predictR < 0.8
%                 predictR = 0.8;
%             elseif predictR < 1
%                 predictR = 1;
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

diff_test_n = R_to_predict - R_hat_n;  
RMSE_test_n = sqrt(mean((diff_test_n(:)).^2,'omitnan'));

% =================================================================================================
% Neighborhood model with User neighbors
% =================================================================================================
% movie similarity matrix
R_tilde = R_train - R_hat;
D_user = zeros(n,n);

for j = 1:n
    for i = 1:n
		if ~(i == j)
			% Compute similarity value
			sum_i_sq = 0;
			sum_j_sq = 0;
			sum_pair = 0;
			for k = 1:m
				if ~isnan(R_tilde(i,k)) && ~isnan(R_tilde(j,k))
					% fprintf('both %d and %d rated movie %d\n', i, j, k);
					sum_pair = sum_pair + R_tilde(i,k) * R_tilde(j,k);
					sum_i_sq = sum_i_sq + R_tilde(i,k) ^ 2;
					sum_j_sq = sum_j_sq + R_tilde(j,k) ^ 2;
				end
			end
			D_user(i,j) = sum_pair/sqrt(sum_i_sq*sum_j_sq);
		else 
			D_user(i,j) = NaN;
		end
	end
end

% r_hat_n for neighborhood model
R_hat_n_user = zeros(n,m);
L = 2; % Variable for number of neighbors that will count in neighborhood model
for j = 1:m 
	for i = 1:n
		if ~isnan(R(i,j)) % Don't really need this if statement, unless we're testing for RMSE 

			% Sum for top 2 movie neighbors to movie j 
			neigh_abs = [(1:n)', abs(D_user(:,i))]; % Store movie neighbors to j and the movie index
			neigh_abs = sortrows(neigh_abs, 2, 'descend'); 
			neigh_abs = neigh_abs(sum(isnan(neigh_abs),2)==0);

			% TODO Calculate neighborhood factor
			% Step 1: Find top L
			sum_dr = 0; % using similarity d as the prediction weight (basic method)
			sum_abs_d = 0;
			for index = 1:min(length(neigh_abs), L) % For neighbor movies, L is limit variable
				% FOR MOVIES
				% n_i = neigh_abs(index);
    %             % fprintf('n_i:%d\n', n_i)
				% if ~isnan(R_tilde(i, n_i))
				% 	% Using similarity d as the weighting
                    
				% 	% fprintf('user: %d, neighbor: %d\n', i, n_i)
				% 	% fprintf('cosine coeff: %d\n', D_movie(j,n_i))
				% 	sum_dr = sum_dr + D_movie(j,n_i) * R_tilde(i,n_i);
				% 	sum_abs_d = sum_abs_d + abs(D_movie(j,n_i));
				% end

				% FOR USERS??? WHAT SHOULD PARAMS BE?
				n_i = neigh_abs(index);
                % fprintf('n_i:%d\n', n_i)
				if ~isnan(R_tilde(n_i, j))
					% Using similarity d as the weighting
                    
					% fprintf('user: %d, neighbor: %d\n', i, n_i)
					% fprintf('cosine coeff: %d\n', D_movie(j,n_i))
					sum_dr = sum_dr + D_user(n_i,i) * R_tilde(n_i,j);
					sum_abs_d = sum_abs_d + abs(D_user(n_i,i));
				end
			end

			% Neighborhood model: Calc normalised weighted sum of weightings 
			if (sum_abs_d == 0) 
				sum_d = 0;
			else
				sum_d = sum_dr/sum_abs_d;
			end

			predictR = r_bar + b_u(i) + b_i(j) + sum_d;
            
            if ~isnan(R_to_predict(i,j))
                if predictR > 1R
                    predictR = 1;
                elseif predictR < 0
                    predictR = 0;
                end
            end
			

			R_hat_n_user(i,j) = predictR;
		else
			R_hat_n_user(i,j) = NaN;
		end
	end
end

% TODO play around with capping in above if predictR > 5 statement
% Check the RMSE compared to training set
diff_train_n_user = R_train - R_hat_n_user;
RMSE_train_n_user = sqrt(mean((diff_train_n_user(:)).^2,'omitnan')); 

diff_test_n_user = R_to_predict - R_hat_n_user;  
RMSE_test_n_user = sqrt(mean((diff_test_n_user(:)).^2,'omitnan'));

% =================================================================================================
% Latent factor (not correct, do on python)
% =================================================================================================

% Start of Latent Fagtor
% TODO: Might want to consider R_tilde/R_hat instead of R?
r_bar_mat = repmat(r_bar, size(R_train));
r_demeaned = R_train - r_bar_mat;
r_demeaned(isnan(r_demeaned))=0;
[U, sigma, vt, flag] = svds(r_demeaned, 40);

% Making predictions from decomposed matrix
r_tilde_latent = U * sigma * vt';
r_hat_latent = r_tilde_latent + r_bar_mat;

% Calculate RMSE
diff_train_latent = R_train - r_hat_latent;
RMSE_train_latent = sqrt(mean((diff_train_latent(:)).^2,'omitnan'));

diff_test_latent = R_to_predict - r_hat_latent;
RMSE_test_latent = sqrt(mean((diff_test_latent(:)).^2,'omitnan'));
% Combining latent factor and neighborhood model
% Making matrix A for training set
[n, m] = size(R_train);
n_ratings = sum(~isnan(R_train(:))); 

A = zeros(n_ratings, 2); % pre-fill for optimisation
c = zeros(n_ratings, 1); % pre-fill for optimisation

rowA = 1; 
for j = 1:m 
	for i = 1:n
		if ~isnan(R_train(i,j))
			A(rowA,1) = R_hat_n(i,j); % Column 1 for neighborhood
			A(rowA,2) = r_hat_latent(i,j); % Column 2 for latent factor 

			c(rowA) = R_train(i,j); 
			
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
% 			if predictR > 5
% 				predictR = 5;
% 			elseif predictR < 1
% 				predictR = 1;
% 			end

			R_hat_c(i,j) = predictR;
		else
			R_hat_c(i,j) = NaN;
		end
	end
end

% Check the RMSE compared to training set
diff_train_c = R_train - R_hat_c;  
RMSE_train_c = sqrt(mean((diff_train_c(:)).^2,'omitnan')); 

diff_test_c = R_to_predict - R_hat_c;  
RMSE_test_c = sqrt(mean((diff_test_c(:)).^2,'omitnan')); 
% weighted sum of models

%new latent
diff_train_l2 = R_to_predict - (P * Q');
RMSE_train_l2 = sqrt(mean((diff_train_l2(:)).^2,'omitnan'));

diff_test_l2 = R_train - (P * Q');
RMSE_test_l2 = sqrt(mean((diff_test_l2(:)).^2,'omitnan'));



fprintf("----Baseline_predictor----\n");
fprintf("RMSE_train %f\n", RMSE_train);
fprintf("RMSE_test %f\n", RMSE_test);

fprintf("----Neighborhood----\n");
fprintf("RMSE_train_n %f\n", RMSE_train_n);
fprintf("RMSE_test_n %f\n", RMSE_test_n);

fprintf("----Neighborhood Users----\n");
fprintf("RMSE_train_n_user %f\n", RMSE_train_n_user);
fprintf("RMSE_test_n_user %f\n", RMSE_test_n_user);

fprintf("----Latent factor----\n");
fprintf("RMSE_train_latent %f\n", RMSE_train_latent);
fprintf("RMSE_test_latent %f\n", RMSE_test_latent);

fprintf("----Combined----\n");
fprintf("RMSE_train_c %f\n", RMSE_train_c);
fprintf("RMSE_test_c %f\n", RMSE_test_c);
fprintf("Script complete\n")
toc