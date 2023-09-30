# Extract a player's primary nation of origin
extract_nation = function(data) {
  nation = data %>%
    dplyr::mutate(
      reg_gp = ifelse(is.na(reg_gp), 0, reg_gp),
      post_gp = ifelse(is.na(post_gp), 0, post_gp)
    ) %>%
    dplyr::group_by(league_nation) %>%
    dplyr::summarize(gp = sum(reg_gp + post_gp), post_gp = sum(post_gp)) %>%
    dplyr::ungroup() %>%
    dplyr::rename(nation_compete = league_nation) %>%
    dplyr::mutate(prop_gp_nation = ifelse(gp == 0 & sum(gp) == 0, 0, gp / sum(gp))) %>%
    dplyr::filter(prop_gp_nation == max(prop_gp_nation)) %>%
    dplyr::arrange(desc(post_gp)) %>%
    head(1) %>%
    dplyr::select(-post_gp, -gp)
  
  if (identical(nation, character(0))) {
    return(NA)
  } else {
    return(nation)
  }
  
}