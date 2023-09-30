# Extract a player's primary league in his draft year
extract_primary_league = function(data) {
  league_name = data %>%
    dplyr::mutate(
      reg_gp = ifelse(is.na(reg_gp), 0, reg_gp),
      post_gp = ifelse(is.na(post_gp), 0, post_gp)
    ) %>%
    dplyr::mutate(gp = reg_gp + post_gp) %>%
    dplyr::arrange(desc(gp), desc(post_gp)) %>%
    head(1) %>%
    dplyr::select(league) %>%
    unlist() %>%
    unname()
  
  if (identical(league_name, character(0))) {
    return("DNP")
  } else {
    return(league_name)
  }
}