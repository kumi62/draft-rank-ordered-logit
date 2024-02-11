
create_static_heatmap = function(simulation_results, player_order) {
  
  pick_range = range(simulation_results$pick)
  
  # Determine pick order for heatmap
  team_order = simulation_results %>%
    arrange(pick) %>%
    select(pick, team) %>%
    unique() %>%
    mutate(team = glue("{pick}. {team}"))
  
  
  # Prepare data for heatmap
  draft_plot_df = expand.grid(player = player_order, pick = pick_range[1]:pick_range[2]) %>%
    left_join(simulation_results %>% select(-team), join_by(player, pick)) %>%
    left_join(team_order, join_by(pick)) %>%
    group_by(player) %>%
    filter(!(max(prob, na.rm = T) == 1 & is.na(prob))) %>%
    ungroup() %>%
    group_by(pick) %>%
    filter(!(max(prob, na.rm = T) == 1 & is.na(prob))) %>%
    ungroup() %>%
    mutate(player = factor(player, levels = player_order)) %>%
    mutate(prob = ifelse(is.na(prob), 0.0000001, prob)) %>%
    mutate(prob_mask = ifelse(prob <= 0.1, prob*10, prob + 0.9)) %>%
    filter(pick <= pick_range[2]) %>%
    mutate(team = factor(team, levels = team_order$team[pick_range[1]:pick_range[2]]))
  
  # Create the static heatmap
  static_heatmap = draft_plot_df %>%
    filter(player %in% head(player_order, pick_range[2])) %>%
    ggplot() +
    geom_tile(aes(x = team, y = player, fill = prob_mask), colour = "grey70") +
    scale_fill_gradientn(
      colours = c("midnightblue", "blue2", "blue", "skyblue", "cyan", "green", "yellow", "gold", "orange", "red", "red2", "red3", "red4"),
      breaks = c(0.00001, 0.5, 1, 1.5, 1.9),
      limits= c(0.00000001,1.9),
      labels = c("0", "0.05", "0.1", "0.5", "1"),
      guide = guide_colorbar(barwidth = 0.8, barheight = 14),
      na.value = "white"
    ) +
    scale_y_discrete(limits=rev, expand = c(0,0)) +
    scale_x_discrete(expand = c(0,0), drop = FALSE) +
    theme_bw() +
    labs(x = "Draft Pick", y = "", fill = "Probability") +
    theme(axis.text.x = element_text(size = 7, angle = 90), axis.text.y = element_text(size = 7)) +
    coord_equal()
  
  if (any(draft_plot_df$prob == 1)) {
    return(
      static_heatmap +
        new_scale_fill() +
        geom_tile(data = . %>% filter(prob == 1), aes(x = team, y = player, fill = "x"), colour = "grey70") +
        scale_fill_manual(values = c("black"), na.value = "transparent", guide = "none")
    )
  } else {
    return(static_heatmap)
  }
  
}