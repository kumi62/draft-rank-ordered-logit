# Extract proportion of games at the Senior level during the draft year
extract_sr_proportion = function(data) {
  agg_data = data %>%
    dplyr::mutate(
      reg_gp = ifelse(is.na(reg_gp), 0, reg_gp),
      post_gp = ifelse(is.na(post_gp), 0, post_gp)
    ) %>%
    dplyr::group_by(league_age_class) %>%
    dplyr::summarize(gp = sum(reg_gp + post_gp)) %>%
    dplyr::ungroup() %>%
    dplyr::rename(age_class = league_age_class) %>%
    dplyr::mutate(sr_games = (age_class == "Senior") * gp + 0.5*(age_class == "College") * gp)
  
  if (sum(agg_data$sr_games) != 0 & sum(agg_data$gp) != 0) {
    prop = sum(agg_data$sr_games) / sum(agg_data$gp)
  } else {
    prop = 0
  }
  
  return(prop)
}