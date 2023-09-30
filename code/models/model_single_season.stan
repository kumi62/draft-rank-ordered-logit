
// User-created functions that are used in the model or generated quantities block
functions{
  
  real luce_lpmf_xyz(int[] x, vector theta, int r, int R, int is_draft) {
    
    // Initialize variables to store the log-likelihood and linear predictor
    real loglik_final; // real number value for the log-likelihood of the ranking set
    vector[r] loglik_vec; // vector with real number values for the log-likelihoods of each rank in the ranking set
    vector[R] eta_vec; // vector with real number values for linear predictor of the jth ranked player
    
    if (is_draft == 0) {
      
      for (j in 1:R) {
        eta_vec[j] = theta[x[j]];
      }
      
    }
    
    // For each ranked player...
    for (i in 1:r) {
      
      // For each available player...
      if (is_draft == 1) {
        for (j in i:R) {
          eta_vec[j] = theta[x[j]];
        }
      }
      
      // Find the log-likelihood of the ith ranked player being in that position
      loglik_vec[i] = categorical_logit_lpmf(1|eta_vec[i:R]);
    }
   
    // Sum up all individual log-likelihoods to obtain final log-likelihood
    loglik_final = sum(loglik_vec);
    return loglik_final;
    
  }

}



// Specifications for the input data to be used in the model
data {
  // BASIC DATA SPECIFICATIONS
  int<lower=1> N; // The total number of ranking sets available
  int<lower=1> P; // The total number of players available over all ranking sets
  int<lower=1> A; // The total number of agencies that provide player rankings or picks
  int<lower=1> R_star; // The maximum number of players available in a single ranking set

  // RANKING SETS
  int is_draft[N]; // A vector containing an indicator for actual NHL draft ranking sets
  int R[N]; // A vector containing the number of players available to be ranked in each ranking set
  int r[N]; // A vector containing the number of players that were ranked in a ranking set
  int x[N,R_star]; // Ranking set data; rows represent a particular ranking set, columns represent a particular rank
  int x_agencies[N,R_star]; // Agency (ranker) data; each row/column combo represents the agency that ranked the corresponding player from x
  
  // COVARIATES
  // Each row/column combo of our covariate matrices correspond to the player in the same row/column of x
  real x_heights[N,R_star]; // A matrix containing the z-scored heights of players involved in the ranking set
  real x_propsr[N,R_star]; // A matrix containing the proportion of GP at Sr level for players involved in the ranking set
  int x_overage[N,R_star]; // A matrix containing indicators for whether or not a player is overaged
  int x_late[N,R_star]; // A matrix containing indicators for whether or not a player is a late birthdate
  int x_usa[N,R_star]; // A matrix containing indicators for whether or not a player is American
  int x_swe[N,R_star]; // A matrix containing indicators for whether or not a player is Swedish
  int x_fin[N,R_star]; // A matrix containing indicators for whether or not a player is Finnish
  int x_rus[N,R_star]; // A matrix containing indicators for whether or not a player is Russian
  int x_eur[N,R_star]; // A matrix containing indicators for whether or not a player is European (non-SWE, FIN, RUS)
  int x_european[N,R_star]; // A matrix containing indicators for whether or not a player is playing in Europe
  
  // PRIOR SCORE
  real prior[P]; // A vector containing the prior theta values in the initial time period
}



// Set model parameters
parameters {
  vector[P-1] theta_raw1; // theta values matrix 1: A (P-1)xT matrix of theta values, we have P-1 rows here as this will be used to obtain a PxT matrix with sum constrained to zero
  real<lower=0> sigma0; // The standard deviation on the prior theta values
}



// Set more model parameters that can be expressed as functions of other parameters
transformed parameters {
  vector[P] theta_raw2 = append_row(theta_raw1, -sum(theta_raw1));
  
  // The final theta matrix (defined below)
  vector[P] theta;

  // Set the thetas in time period 1 to be the prior value for the particular player + the random component defined by theta_raw2
  theta = to_vector(prior) + theta_raw2*sigma0;
}



// Specify the likelihood and priors for the ROL model
model {
  //// LIKELIHOOD ////
  vector[N] out;
  
  for (i in 1:N) {
    out[i] = luce_lpmf_xyz(x[i,:], theta, r[i], R[i], is_draft[i]);
  }
  
  target += sum(out);
  
  
  //// PRIORS ////
  sigma0 ~ inv_gamma(2.0, 1.0);
  theta_raw2 ~ normal(0.0, 1.0);
}


