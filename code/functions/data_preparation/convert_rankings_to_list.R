# Convert data frame into list that is compatible with our Stan models
convert_rankings_to_list = function(rankings, agencies, prior, player_data_model, include_prior = TRUE) {
  # Create matrix of player IDs for each ranking set (row) and rank (col)
  rankings_matrix = rankings %>%
    dplyr::select(resource_id, ranking) %>%
    tidyr::unnest(ranking) %>%
    dplyr::mutate_at(vars(starts_with("Rank_")), function(x) {tidyr::replace_na(x,0)}) %>%
    column_to_rownames("resource_id")
  
  # Create matrix of ranker IDs for each ranking set (row) and rank (col)
  agencies_matrix = rankings %>%
    dplyr::select(resource_id, agencies) %>%
    tidyr::unnest(agencies) %>%
    dplyr::mutate_at(vars(starts_with("Agency_")), function(x) {tidyr::replace_na(x,0)}) %>%
    tibble::column_to_rownames("resource_id")
  
  # Create matrix of player z-scored heights for each ranking set (row) and rank (col)
  height_z_matrix = rankings_matrix %>%
    dplyr::rowwise() %>%
    dplyr::mutate_all(function(x) {ifelse(x == 0, 0, player_data_model$height_z[player_data_model$stan_id == x])}) %>%
    dplyr::ungroup()
  
  # Create matrix of player proportion of games at Sr level for each ranking set (row) and rank (col)
  prop_sr_matrix = rankings_matrix %>%
    dplyr::rowwise() %>%
    dplyr::mutate_all(function(x) {ifelse(x == 0, 0, player_data_model$prop_sr[player_data_model$stan_id == x])}) %>%
    dplyr::ungroup()
  
  # Create boolean matrix for whether a player is overaged or not for each ranking set (row) and rank (col)
  is_overage_matrix = rankings_matrix %>%
    dplyr::rowwise() %>%
    dplyr::mutate_all(function(x) {ifelse(x == 0, 0, player_data_model$age_split[player_data_model$stan_id == x] == "Overage")}) %>%
    dplyr::ungroup() %>%
    dplyr::mutate_all(as.numeric)
  
  # Create boolean matrix for whether a player is a late birthdate or not for each ranking set (row) and rank (col)
  is_late_bday_matrix = rankings_matrix %>%
    dplyr::rowwise() %>%
    dplyr::mutate_all(function(x) {ifelse(x == 0, 0, player_data_model$age_split[player_data_model$stan_id == x] == "Late")}) %>%
    dplyr::ungroup() %>%
    dplyr::mutate_all(as.numeric)
  
  # Create boolean matrix for whether a player is American or not for each ranking set (row) and rank (col)
  is_usa = rankings_matrix %>%
    dplyr::rowwise() %>%
    dplyr::mutate_all(function(x) {ifelse(x == 0, 0, player_data_model$nation_origin[player_data_model$stan_id == x] == "USA")}) %>%
    dplyr::ungroup() %>%
    dplyr::mutate_all(as.numeric)
  
  # Create boolean matrix for whether a player is Swedish or not for each ranking set (row) and rank (col)
  is_swe = rankings_matrix %>%
    dplyr::rowwise() %>%
    dplyr::mutate_all(function(x) {ifelse(x == 0, 0, player_data_model$nation_origin[player_data_model$stan_id == x] == "SWE")}) %>%
    dplyr::ungroup() %>%
    dplyr::mutate_all(as.numeric)
  
  # Create boolean matrix for whether a player is Finnish or not for each ranking set (row) and rank (col)
  is_fin = rankings_matrix %>%
    dplyr::rowwise() %>%
    dplyr::mutate_all(function(x) {ifelse(x == 0, 0, player_data_model$nation_origin[player_data_model$stan_id == x] == "FIN")}) %>%
    dplyr::ungroup() %>%
    dplyr::mutate_all(as.numeric)
  
  # Create boolean matrix for whether a player is Russian or not for each ranking set (row) and rank (col)
  is_rus = rankings_matrix %>%
    dplyr::rowwise() %>%
    dplyr::mutate_all(function(x) {ifelse(x == 0, 0, player_data_model$nation_origin[player_data_model$stan_id == x] == "RUS")}) %>%
    dplyr::ungroup() %>%
    dplyr::mutate_all(as.numeric)
  
  # Create boolean matrix for whether a player is (non-RUS, FIN, or SWE) European or not for each ranking set (row) and rank (col)
  is_eur = rankings_matrix %>%
    dplyr::rowwise() %>%
    dplyr::mutate_all(function(x) {ifelse(x == 0, 0, player_data_model$nation_origin[player_data_model$stan_id == x] == "EUR")}) %>%
    dplyr::ungroup() %>%
    dplyr::mutate_all(as.numeric)
  
  is_european = rankings_matrix %>%
    dplyr::rowwise() %>%
    dplyr::mutate_all(function(x) {ifelse(x == 0, 0, player_data_model$continent[player_data_model$stan_id == x] == "Europe")}) %>%
    dplyr::ungroup() %>%
    dplyr::mutate_all(as.numeric)
  
  
  
  # Assemble data into a list
  stan_dt = list(
    # Number of ranking sets (N) and players (P)
    N = nrow(rankings_matrix),
    P = nrow(player_data_model),
    A = nrow(agencies),
    # Maximum number of players that can be ranked
    R_star = ncol(rankings_matrix),
    r = unlist(rankings$n_ranked),
    R = unlist(rankings$n_pool),
    is_draft = unlist(rankings$is_draft),
    # Rankings, agencies and covariates
    x = as.matrix(rankings_matrix),
    x_agencies = as.matrix(agencies_matrix),
    x_heights = as.matrix(height_z_matrix),
    x_propsr = as.matrix(prop_sr_matrix),
    x_overage = as.matrix(is_overage_matrix),
    x_late = as.matrix(is_late_bday_matrix),
    x_usa = as.matrix(is_usa),
    x_rus = as.matrix(is_rus),
    x_swe = as.matrix(is_swe),
    x_fin = as.matrix(is_fin),
    x_eur = as.matrix(is_eur),
    x_european = as.matrix(is_european)
  )
  
  if (include_prior) {
    return(stan_dt %>% append(list(prior = prior$score)))
  } else {
    return(stan_dt)
  }
  
}