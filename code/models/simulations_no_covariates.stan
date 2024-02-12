
// OBJECTIVE
//   Use posterior samples of model parameters to simulate the remainder of the draft
//   This function provides customization to run simulations based the following options:
//     - After Each Pick of Draft with Team Tendency Parameters
//     - After Each Pick of Draft without Team Tendency Parameters
//     - Single Moment of Draft with Team Tendency Parameters
//     - Single Moment of Draft without Team Tendency Parameters

functions {
  
  // This function is designed to be used within the simulate_draft function specified below
  // The goal is to find the choice probabilities for each player given the remaining players available to be drafted
  vector find_choice_probs(vector eta, int P_available, int P, int[] picked_players, int pick_number){
    
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
    
    // Determine the choice probabilities for all available players
    choice_probs = exp_remaining_etas / sum(exp_remaining_etas);
    
    // Return the choice probabilities for all available players
    return choice_probs;
    
 }
 
  // Simulate the NHL draft forward given previous picks
  int[,] draft_moment_rng(vector theta, int[] selected, int[] available, int[] teams, int m, int M, int P_available, int P) {
   
    int draft_order[M,1];
    vector[P] choice_probs;
    vector[P] eta;
   
    for (k in 1:P) {
      eta[k] = 0.0;
    }
   
    // For each pick...
    for (i in 1:M) {
     
      if (i <= m) {
        draft_order[i,1] = selected[i];
      } else {
       
        for (j in 1:P_available) {
          eta[available[j]] = theta[available[j]];
        }
       
        if (i != 1) {
          choice_probs = find_choice_probs(eta, P_available, P, draft_order[1:(i-1),1], i);
        } else {
          choice_probs = softmax(eta);
        }
       
        draft_order[i,1] = categorical_rng(choice_probs);
       
      }
    }
   
    return draft_order;
   
  }
  
  // Simulate the NHL draft forward given previous picks
  int[,] draft_start_rng(vector theta, int[] available, int[] teams, int M, int P_available, int P) {
   
    int draft_order[M,1];
    vector[P] choice_probs;
    vector[P] eta;
   
    for (k in 1:P) {
      eta[k] = 0.0;
    }
    
    // For each pick...
    for (i in 1:M) {
      
      for (j in 1:P_available) {
        eta[available[j]] = theta[available[j]];
      }
      
      if (i != 1) {
        choice_probs = find_choice_probs(eta, P_available, P, draft_order[1:(i-1), 1], i);
      } else {
        choice_probs = softmax(eta);
      }
        
      draft_order[i,1] = categorical_rng(choice_probs);
     
    }
    
    return draft_order;
    
  }
 
  // Simulate the NHL draft after each pick that is made
  int[,] draft_retrospective_rng(vector theta, int[] selected, int[] available, int[] teams, int m, int M, int P_available, int P) {
    
     // Initialize variables to store draft order and all intermediate calculations
     int draft_order[M,m+1];
     vector[P] choice_probs;
     vector[P] eta;
     
     for (k in 1:P) {
       eta[k] = 0.0;
     }
     
     for (L in 0:m) {
       
       for (i in 1:M) {
        
        if (i <= L) {
          draft_order[i,L+1] = selected[i];
        } else {
          
          for (j in 1:P_available) {
            eta[available[j]] = theta[available[j]];
          }
          
          for (j in 1:m) {
            eta[selected[j]] = theta[selected[j]];
          }
          
          if (i != 1) {
            choice_probs = find_choice_probs(eta, P_available, P, draft_order[1:(i-1),L+1], i);
          } else {
            choice_probs = softmax(eta);
          }
          
          draft_order[i,L+1] = categorical_rng(choice_probs);
          
        }
       }
    }
    
    return draft_order;
  }
 
  // Run appropriate rng function
  int[,] draft_rng(vector theta, int[] selected, int[] available, int[] teams, int m, int M, int P_available, int P, int is_retrospective) {
    
    int draft_order[M,is_retrospective == 1 ? m+1 : 1];
    
    if (is_retrospective == 1) {
      draft_order = draft_retrospective_rng(
        theta,
        selected,
        available,
        teams,
        m,
        M,
        P_available,
        P
      );
    } else if (m == 1 && selected[1] == 0) {
      draft_order = draft_start_rng(
        theta,
        available,
        teams,
        M,
        P_available,
        P
      );
    } else {
      draft_order = draft_moment_rng(
        theta,
        selected,
        available,
        teams,
        m,
        M,
        P_available,
        P
      );
    }
    
    return draft_order;
  }
 
}


// Specifications for the input data to be used in the model
data {
  
  int<lower=1> P; // The total number of players available over all ranking sets
  int<lower=1> P_available; // The total number of players available in the current year
  int<lower=1> A; // The total number of agencies and teams in the data
  
  int<lower=0,upper=1> is_retrospective; // Indicator for whether to run sims after each pick in `selected` or just run once after all picks in `selected`
  
  int n_picks_total;
  int n_picks_made;
  int selected[n_picks_made];
  int available[P_available];
  int teams[n_picks_total];
  
}



// Set model parameters
parameters {
  vector[P] theta;
}



// Use posterior draws to simulate the NHL draft
generated quantities {
  
  // Initialize variable to store simulated draft results
  int draft_sim[n_picks_total, is_retrospective == 1 ? n_picks_made + 1 : 1];
  
  // Simulate the NHL draft
  draft_sim = draft_rng(theta, selected, available, teams, n_picks_made, n_picks_total, P_available, P, is_retrospective);
  
}

