# Create a resource ID code for each ranking set (i.e., "2015_TSN_1", "2022_Sportsnet_6", ...)
set_resource_id = function(resource_site,
                           year,
                           resource_date,
                           league_subset,
                           region_subset,
                           position_subset,
                           nationality_subset) {
  orig_df = data.frame(
    resource_site,
    year,
    resource_date,
    league_subset,
    region_subset,
    position_subset,
    nationality_subset
  ) 
  
  new_df = orig_df %>%
    dplyr::distinct() %>%
    dplyr::mutate(league_subset2 = tidyr::replace_na(league_subset, "")) %>%
    dplyr::mutate(region_subset2 = tidyr::replace_na(region_subset, "")) %>%
    dplyr::mutate(position_subset2 = tidyr::replace_na(position_subset, "")) %>%
    dplyr::mutate(nationality_subset2 = tidyr::replace_na(nationality_subset, "")) %>%
    dplyr::mutate(resource_site2 = stringr::str_replace_all(resource_site, " ", "-")) %>%
    dplyr::mutate(resource_site2 = stringr::str_replace_all(resource_site2, "_", "-")) %>%
    dplyr::group_by(resource_site2, year) %>%
    dplyr::arrange(
      resource_site2,
      year,
      resource_date,
      league_subset2,
      region_subset2,
      position_subset2,
      nationality_subset2
    ) %>%
    dplyr::mutate(ones = 1) %>%
    dplyr::mutate(order = cumsum(ones)) %>%
    dplyr::mutate(resource_id = paste(year, resource_site2, order, sep = "_")) %>%
    dplyr::ungroup() %>%
    dplyr::select(-ones, -order, -resource_site2) %>%
    dplyr::mutate_at(vars(ends_with("subset")), ~tidyr::replace_na(., "NA"))
  
  final_df = orig_df %>%
    dplyr::mutate_at(vars(ends_with("subset")), ~tidyr::replace_na(., "NA")) %>%
    dplyr::left_join(
      new_df,
      dplyr::join_by(
        resource_site,
        year,
        resource_date,
        league_subset,
        region_subset,
        position_subset,
        nationality_subset
      )
    )
  
  return(final_df$resource_id)
}