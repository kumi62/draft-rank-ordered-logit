
create_player_cdf = function(simulation_results, player_name) {
  
  n_picks_made = simulation_results %>%
    filter(prob == 1) %>%
    select(pick) %>%
    max()
  
  n_picks_simmed = simulation_results %>%
    select(pick) %>%
    max()
  
  # Extract player's CDF
  player_cdf = expand.grid(player = player_name, pick = 1:max(simulation_results$pick)) %>%
    left_join(simulation_results, join_by(player, pick)) %>%
    ungroup() %>%
    
    arrange(pick) %>%
    mutate(
      is_pick_made = ifelse(pick <= n_picks_made, "Yes", "No") %>% factor(levels = c("Yes", "No")),
      prob = ifelse(is.na(prob), 0, prob),
      cumul_prob_available = 1 - cumsum(prob),
    )
  
  # Plot pmf of player's pick distribution
  cdf_plot = ggplot(player_cdf) +
    geom_bar(aes(x = pick, y = cumul_prob_available, fill = is_pick_made), stat = "identity", colour = "black", alpha = 0.75) +
    #geom_vline(xintercept = 15, colour = "forestgreen", size = 1.25) +
    #geom_vline(xintercept = 23, colour = "red", size = 1.25) +
    #geom_vline(xintercept = 47, colour = "forestgreen", size = 1.25) +
    labs(x = "Draft Pick", y = glue("Probability {player_name} is Available"), fill = "Has the pick\nbeen made?") +
    theme_bw() +
    scale_x_continuous(expand = c(0,0), breaks = seq(5, n_picks_simmed, 5), limits = c(1 - 0.75, n_picks_simmed + 0.75)) +
    scale_y_continuous(expand = c(0,0), limits = c(-0.005,1.005)) +
    theme(
      panel.grid = element_blank(),
      axis.text = element_text(size = 14, family = "Arial Narrow"), 
      axis.title = element_text(size = 14),
      legend.text = element_text(size = 14),
      legend.title = element_text(size = 14)
    )
  
  return(cdf_plot)
}
