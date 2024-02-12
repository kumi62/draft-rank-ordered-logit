# Convert player names to IDs
player2id = function(players, player_data, year) {
  
  data.frame(player = players) %>%
    left_join(player_data %>% filter(draft_year == year), by = "player") %>%
    select(stan_id) %>%
    unlist() %>%
    unname()
  
}