# Extract a player's primary region in his draft year
extract_primary_region = function(data, year) {
  region_name = data %>%
    dplyr::mutate(
      reg_gp = ifelse(is.na(reg_gp), 0, reg_gp),
      post_gp = ifelse(is.na(post_gp), 0, post_gp)
    ) %>%
    dplyr::group_by(league_region) %>%
    dplyr::summarize(gp = sum(reg_gp + post_gp), post_gp = sum(post_gp)) %>%
    dplyr::ungroup() %>%
    dplyr::arrange(desc(gp), desc(post_gp)) %>%
    head(1) %>%
    dplyr::select(league_region) %>%
    unlist() %>%
    unname()
  
  if (identical(region_name, character(0))) {
    return("DNP")
  } else {
    return(region_name)
  }
}