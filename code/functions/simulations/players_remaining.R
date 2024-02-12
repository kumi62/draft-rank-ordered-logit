# Obtain undrafted player IDs given drafted players and year
players_remaining = function(selected_players, player_data, year) {
  
  player_data %>%
    filter((draft_year == year) & !(stan_id %in% selected_players)) %>%
    select(stan_id) %>%
    unlist() %>%
    unname()
  
}