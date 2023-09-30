# Convert agency data into a single row of agencies (ie drafting teams)
prep_agencies = function(ranking, unranked_players) {
  ranking %>%
    dplyr::mutate(rank = as.numeric(rank)) %>%
    dplyr::arrange(rank) %>%
    dplyr::select(agency_id) %>%
    dplyr::bind_rows(data.frame(agency_id = rep(0, nrow(unranked_players)))) %>%
    t() %>%
    as.data.frame() %>%
    magrittr::set_colnames(paste0("Agency_", 1:ncol(.)))
}