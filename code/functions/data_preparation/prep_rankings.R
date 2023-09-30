# Flatten each ranking set into a single row of ranks
prep_rankings = function(ranking, unranked_players) {
  ranking %>%
    dplyr::mutate(rank = as.numeric(rank)) %>%
    dplyr::arrange(rank) %>%
    dplyr::bind_rows(unranked_players) %>%
    dplyr::select(stan_id) %>%
    t() %>%
    as.data.frame() %>%
    magrittr::set_colnames(paste0("Rank_", 1:ncol(.)))
}