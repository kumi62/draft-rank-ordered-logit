
// MODEL 1
//  Builds upon Model 1 by
//    - Simulating the draft after each pick rather than just from the start (allows us to make the gif)

// User-created functions that are used in the model or generated quantities block
functions{
  
  // This function is designed to be used within the simulate_draft function specified below
  // The goal is to find the choice probabilities for each player given the remaining players available to be drafted
  vector find_choice_probs(vector eta, int P_available, int P_unavailable, int P, int[] picked_players, int[] unavailable, int pick_number){
    
    // Initialize variables to store the choice probabilities and various intermediate calculations
    vector[P] exp_remaining_etas;
    vector[P] choice_probs;
    real denom;
    denom = 0.0;
    
    // Determine exp(theta_i) for all player i's
    exp_remaining_etas = exp(eta);
    
    // For all previous picks...
    for (i in 1:(pick_number - 1)) {
      // Set their exp(theta) value to zero (i.e. remove them as an option to be picked next)
      exp_remaining_etas[picked_players[i]] = 0.0;
    }
    
    // For all unavailable players...
    for (j in 1:P_unavailable) {
      exp_remaining_etas[unavailable[j]] = 0.0;
    }
    
    // Determine the choice probabilities for all available players
    choice_probs = exp_remaining_etas / sum(exp_remaining_etas);
    
    // Return the choice probabilities for all available players
    return choice_probs;
    
 }
 
 // Simulate the NHL draft forward given previous picks
 int[] draft_rng(vector theta, int[] selected, int[] available, int[] unavailable, int[] teams, int m, int M, int P_available, int P_unavailable, int P) {
   
   int draft_order[M];
   vector[P] choice_probs;
   vector[P] eta;
   
   for (k in 1:P) {
     eta[k] = 0.0;
   }
   
   for (L in 1:P_unavailable) {
     eta[unavailable[L]] = -100.0;
   }
   
   // For each pick...
   for (i in 1:M) {
     
     if (i <= m) {
       draft_order[i] = selected[i];
     } else {
       
       for (j in 1:P_available) {
         eta[available[j]] = theta[available[j]];
       }
       
       if (i != 1) {
         choice_probs = find_choice_probs(eta, P_available, P_unavailable, P, draft_order[1:(i-1)], unavailable, i);
       } else {
         choice_probs = softmax(eta);
       }
       
       draft_order[i] = categorical_rng(choice_probs);
       
     }
     
   }
   
   return draft_order;
   
 }
  
 // Simulate the NHL draft forward given previous picks
 int[] draft_start_rng(vector theta, int[] available, int[] unavailable, int[] teams, int M, int P_available, int P_unavailable, int P) {
   
   int draft_order[M];
   vector[P] choice_probs;
   vector[P] eta;
   
   for (k in 1:P) {
     eta[k] = 0.0;
   }
   
   for (L in 1:P_unavailable) {
     eta[unavailable[L]] = -100.0;
   }
   
   // For each pick...
   for (i in 1:M) {
     
     for (j in 1:P_available) {
       eta[available[j]] = theta[available[j]];
     }
     
     if (i != 1) {
       choice_probs = find_choice_probs(eta, P_available, P_unavailable, P, draft_order[1:(i-1)], unavailable, i);
     } else {
       choice_probs = softmax(eta);
     }
       
     draft_order[i] = categorical_rng(choice_probs);
    
   }
   
   return draft_order;
   
 }
  
  
}


// Specifications for the input data to be used in the model
data {
  
  int<lower=1> P; // The total number of players available over all ranking sets
  int<lower=1> P_available; // The total number of players available in the current year
  int<lower=1> P_unavailable; // The total number of players from the other draft years
  int<lower=1> A; // The total number of agencies and teams in the data
  
  int n_picks_total;
  int n_picks_made;
  int selected[n_picks_made];
  int available[P_available];
  int unavailable[P_unavailable];
  real heights[P];
  real propsr[P];
  int overage[P];
  int teams[n_picks_total];
  
}


// Set model parameters
parameters {
  
  vector[P] theta;
}




// Use posterior draws from theta to simulate the NHL draft
generated quantities {
  
  //vector[P] theta = [theta1, theta2, theta3, theta4, theta5, theta6, theta7, theta8, theta9, theta10]';
  
  
  // Initialize variable to store simulated draft results
  int draft_sim[n_picks_total];
  
  // Simulate the NHL draft
  draft_sim = draft_rng(theta, selected, available, unavailable, teams, n_picks_made, n_picks_total, P_available, P_unavailable, P);
  
}

