
source("code/functions/simulations/player2id.R")
source("code/functions/simulations/agency2id.R")
source("code/functions/simulations/players_remaining.R")

draft_simulator = function(model,
                           player_data,
                           agency_data,
                           draft_results,
                           picks_made,
                           n_picks_shown = 32,
                           n_players_shown = 32,
                           year,
                           include_covariates = TRUE,
                           is_retrospective = FALSE) {
  
  # Extract the draft order by team picking
  draft_order = draft_results %>%
    filter(year == year) %>%
    arrange(rank) %>%
    select(team) %>%
    unlist() %>%
    .[1:n_picks_shown] %>%
    agency2id(agency_data, year)

  # Obtain ordered vector of selected player IDs
  if (length(picks_made) > 0) {
    if (is.numeric(picks_made)) {
      selected = picks_made
    } else {
      selected = player2id(picks_made, player_data, year)
    }
  } else {
    selected = c()
  }
  
  # Adjust to make simulations compatible to cases with 0 or 1 picks assumed
  if (length(selected) == 1) {
    selected = array(selected, dim = 1)
  } else if (length(selected) == 0) {
    selected = array(c(0), dim = 1)
  }
  
  if (NA %in% selected) {
    stop("At least one player in picks_made does not map to a stan_id")
  }
  
  # Obtain vector of pool of remaining player IDs
  pool = players_remaining(selected, player_data, year)
  
  # Obtain vector of players from other draft years
  unavailable = player_data %>%
    filter(draft_year != year) %>%
    select(stan_id) %>%
    unlist() %>%
    unname()
  
  # Extract player-level covariates
  heights = player_data$height_z
  overage = as.numeric(player_data$age_split == "Overage")
  propsr = player_data$prop_sr
  
  # Put relevant data in a list
  draft_data = list(
    P = nrow(player_data),
    P_available = length(pool),
    P_unavailable = length(unavailable),
    A = nrow(agency_data),
    is_retrospective = as.numeric(is_retrospective),
    n_picks_total = n_picks_shown,
    n_picks_made = length(selected),
    selected = selected,
    available = pool,
    unavailable = unavailable,
    heights = heights,
    propsr = propsr,
    overage = overage,
    teams = draft_order
  )
  
  # Extract posterior samples from model
  posterior_draws = as.matrix(model)
  
  
  if (include_covariates) {
    # Simulate the draft given model draws
    simulation_with_covariates = stan_model("code/models/simulations_with_covariates.stan")
    
    sims = simulation_with_covariates %>%
      gqs(data = draft_data, draws = posterior_draws) %>%
      as.matrix() %>%
      as.data.frame()
  } else {
    # Simulate the draft given model draws
    simulation_no_covariates = stan_model("code/models/simulations_no_covariates.stan")
    
    sims = simulation_no_covariates %>%
      gqs(data = draft_data, draws = posterior_draws) %>%
      as.matrix() %>%
      as.data.frame()
  }
  
  
  # Obtain number of simulations
  n_sims = nrow(sims)
  
  # Create PMFs for each player/pick combo
  pmfs = sims %>%
    select(starts_with("draft_sim")) %>%
    rownames_to_column("simulation") %>%
    mutate(simulation = as.numeric(simulation)) %>%
    pivot_longer(cols = starts_with("draft_sim"), names_to = "sim_index", values_to = "stan_id") %>%
    mutate(stan_id = as.numeric(stan_id)) %>%
    left_join(player_data %>% select(player, stan_id), by = "stan_id") %>%
    mutate(sim_index = str_remove(sim_index, "draft_sim\\[")) %>%
    mutate(sim_index = str_remove(sim_index, "\\]")) %>%
    separate(sim_index, into = c("pick", "pick_sim_start"), sep = ",") %>%
    mutate(pick = as.numeric(pick)) %>%
    mutate(pick_sim_start = as.numeric(pick_sim_start)) %>%
    group_by(player, pick, pick_sim_start) %>%
    tally() %>%
    ungroup() %>%
    mutate(prob = n / n_sims) %>%
    select(player, pick, pick_sim_start, prob) %>%
    mutate(
      player = as.character(player),
      pick = as.numeric(pick)
    ) %>%
    left_join(
      draft_results %>%
        rename(draft_year = year) %>%
        filter(draft_year == year) %>%
        select(rank, team),
      join_by(pick == rank)
    )
  
  if (!is_retrospective) {
    pmfs = pmfs %>%
      select(-pick_sim_start)
  }
  
  return(pmfs)
  
}