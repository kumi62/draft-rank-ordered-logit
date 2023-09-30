# Extract primary age class and proportion of games at that age class
extract_age_class = function(data) {
  data %>%
    dplyr::mutate(
      reg_gp = ifelse(is.na(reg_gp), 0, reg_gp),
      post_gp = ifelse(is.na(post_gp), 0, post_gp)
    ) %>%
    dplyr::group_by(league_age_class) %>%
    dplyr::summarize(gp = sum(reg_gp + post_gp), post_gp = sum(post_gp)) %>%
    dplyr::ungroup() %>%
    dplyr::rename(age_class = league_age_class) %>%
    dplyr::mutate(prop_gp_age_class = ifelse(gp == 0 & sum(gp) == 0, 0, gp / sum(gp))) %>%
    dplyr::filter(prop_gp_age_class == max(prop_gp_age_class)) %>%
    dplyr::arrange(desc(post_gp)) %>%
    head(1) %>%
    dplyr::select(-post_gp, -gp)
}