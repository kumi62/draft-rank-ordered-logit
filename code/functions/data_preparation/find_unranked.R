# Find all players who are unranked in a ranking set
find_unranked = function(ranking,
                         year,
                         league_subset = NA,
                         region_subset = NA,
                         position_subset = NA,
                         nationality_subset = NA) {
  players = player_data_model %>%
    dplyr::filter(draft_year == year)
  
  if (!is.na(league_subset)) {
    players = players %>%
      dplyr::filter(primary_league == league_subset)
  }
  
  if (!is.na(region_subset)) {
    if (region_subset %in% c("North America", "Europe")) {
      players = players %>%
        dplyr::filter(continent == region_subset)
    } else {
      players = players %>%
        dplyr::filter(primary_region == region_subset)
    }
  }
  
  if (!is.na(position_subset)) {
    if (position_subset == "Forwards") {
      players = players %>%
        dplyr::filter(pos_broad == "F")
    } else if (position_subset == "Defencemen") {
      players = players %>%
        dplyr::filter(pos_broad == "D")
    } else if (position_subset == "Goalies") {
      players = players %>%
        dplyr::filter(pos_broad == "G")
    } else if (position_subset == "Skaters") {
      players = players %>%
        dplyr::filter(pos_broad %in% c("F", "D"))
    }
    
  }
  
  if (!is.na(nationality_subset)) {
    nationality_adj = dplyr::case_when(
      nationality_subset == "Sweden" ~ "SWE",
      nationality_subset == "Canada" ~ "CAN",
      nationality_subset == "USA" ~ "USA",
      nationality_subset == "Russia" ~ "RUS",
      nationality_subset == "Finland" ~ "FIN",
      nationality_subset == "Europe" ~ "EUR"
    )
    
    if (is.na(nationality_adj)) {
      warning(paste("Nationality", nationality_subset, "not found!"))
    }
    
    players = players %>%
      dplyr::filter(nation_origin == nationality_adj)
  }
  
  players = players %>%
    dplyr::filter(!(stan_id %in% ranking$stan_id))
  
  return(
    players %>%
      dplyr::select(stan_id) %>%
      dplyr::arrange(stan_id)
  )
}