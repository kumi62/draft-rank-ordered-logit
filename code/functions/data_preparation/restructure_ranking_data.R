# Reformat model data frame to be in structure that is compatible with Stan model
source("code/functions/data_preparation/find_unranked.R")
source("code/functions/data_preparation/prep_agencies.R")
source("code/functions/data_preparation/prep_rankings.R")

restructure_ranking_data = function(ranking_data_full, player_data_model, output_prior = TRUE) {
  ## CLEAN UP AGENCY NAMES ##
  rankings_model_v1 = ranking_data_full %>%
    # Select draft rankings from reliable sources
    dplyr::filter(set_type %in% c("rank", "results")) %>%
    dplyr::filter(!(resource_site %in% c("Tout Sur Le Hockey", "SB Nation"))) %>%
    # Rename ranking set resource_id for actual NHL draft results
    dplyr::mutate(resource_id = ifelse(set_type == "results", paste0(year, "_NHL_Draft"), resource_id)) %>%
    # Create a ranker name variable
    dplyr::mutate(
      agency_name = ifelse(set_type == "results", team, paste(resource_site, "-", resource_staff)),
      agency_type = ifelse(set_type == "results", "team", "resource"),
      team = ifelse(set_type == "results", team, NA),
      resource_site = ifelse(set_type == "results", NA, resource_site)
    ) %>%
    dplyr::mutate(agency_name = dplyr::case_when(
      agency_name == "Dobber Prospects - Cam Robinson" ~ "Elite Prospects - Cam Robinson",
      agency_name == "Raw Charge - Lauren Kelly" ~ "Elite Prospects - Lauren Kelly",
      agency_name == "ESPN - Chris Peters" ~ "Daily Faceoff - Chris Peters",
      TRUE ~ agency_name
    )) %>%
    # Remove unwanted ranks
    dplyr::filter(is.na(nationality_subset) & is.na(league_subset)) %>%
    dplyr::filter(!(agency_name %in% c(
      "The Puck Authority - Full Staff", "Elite Prospects - Lauren Kelly", "NHL.com - Mike G. Morreale",
      "ISS Hockey - Full Staff", "Dobber Prospects - Tony Ferrari", "Elite Prospects - Dylan Griffing",
      "Elite Prospects - Mitch Brown", "Elite Prospects - J.D. Burke"
    ))) %>%
    # Create a ranker ID variable
    dplyr::arrange(agency_type, agency_name) %>%
    dplyr::mutate(agency_id = agency_name %>% factor(levels = unique(agency_name)) %>% as.numeric())
  
  # Extract all unique agencies and IDs
  agencies = rankings_model_v1 %>%
    dplyr::select(agency_id, agency_type, agency_name) %>%
    unique()
  
  # Prepare ranking data for modelling
  rankings_model_v2 = rankings_model_v1 %>%
    # Select relevant columns
    dplyr::select(
      resource_id, resource_site, resource_staff, agency_id, resource_date, year,
      league_subset, region_subset, position_subset, nationality_subset,
      rank, stan_id, set_type
    ) %>%
    dplyr::group_by(agency_id, year) %>%
    # Determine if the ranking was final (after season & last ranking by agency)
    dplyr::mutate(is_final = ifelse(
      lubridate::ymd(resource_date) == max(lubridate::ymd(resource_date)) &
        resource_date %>% lubridate::ymd() %>% lubridate::month() >= 4 &
        resource_date %>% lubridate::ymd() %>% lubridate::year() == year,
      TRUE,
      FALSE
    )) %>%
    dplyr::ungroup() %>%
    # Convert ranks to numeric
    dplyr::mutate(rank = as.numeric(rank)) %>%
    # Nest the ranking data
    tidyr::nest(ranking = c(rank, agency_id, stan_id)) %>%
    dplyr::mutate(
      # Determine number of players ranked
      n_ranked = purrr::map(ranking, ~nrow(.x)),
      # Nest in player data (for use in creating list of unranked players)
      player_data = purrr::map(1, ~player_data_model),
      # Determine unranked players
      unranked_players = purrr::pmap(list(ranking, player_data, year, league_subset, region_subset, position_subset, nationality_subset), find_unranked),
      # Convert agencies into single rows
      agencies = purrr::map2(ranking, unranked_players, prep_agencies),
      # Convert rankings into single rows
      ranking = purrr::map2(ranking, unranked_players, prep_rankings),
      # Determine number of players in the available pool to be ranked
      n_pool = purrr::map(ranking, ~ncol(.x))
    ) %>%
    dplyr::arrange(resource_date) %>%
    # Create variable to label ranks vs results
    dplyr::mutate(is_draft = as.integer(ifelse(set_type == "results", 1, 0))) %>%
    # Select relevant columns
    dplyr::select(
      resource_id, resource_site, resource_staff, resource_date, year, is_draft, is_final,
      league_subset, region_subset, position_subset, nationality_subset,
      n_ranked, n_pool, ranking, agencies
    )
  
  
  # Split period 0 (used for prior) from the rest of the data (used for model)
  old_just_rank = rankings_model_v2 %>%
    dplyr::filter(!is_final) %>%
    dplyr::filter(is.na(league_subset) & is.na(position_subset) & is.na(region_subset) & is.na(nationality_subset)) %>%
    dplyr::select(-agencies) %>%
    dplyr::mutate(ranking = purrr::map2(ranking, n_ranked, ~.x[,1:.y])) %>%
    tidyr::unnest(c(n_ranked, n_pool, ranking))
  
  old_unranked = rankings_model_v2 %>%
    dplyr::filter(!is_final) %>%
    dplyr::filter(is.na(league_subset) & is.na(position_subset) & is.na(region_subset) & is.na(nationality_subset)) %>%
    dplyr::select(-agencies) %>%
    tidyr::unnest(c(n_ranked, n_pool, ranking))
  
  rankings_model_v3 = rankings_model_v2 %>%
    dplyr::filter(is_final)
  
  # Set prior theta values for time period 1
  theta_prior = player_data_model %>%
    dplyr::select(stan_id, player, draft_year) %>%
    # Count of 1st overall ranks
    dplyr::mutate(num1 = purrr::map(stan_id, ~length(which(old_just_rank$Rank_1 == .x)))) %>%
    # Count of 2nd-5th ranks
    dplyr::mutate(top5 = purrr::map(stan_id, ~length(which(old_just_rank %>% select(num_range("Rank_", 2:5)) == .x)))) %>%
    # Count of 6th-32nd ranks
    dplyr::mutate(top32 = purrr::map(stan_id, ~length(which(old_just_rank %>% select(num_range("Rank_", 6:32)) == .x)))) %>%
    # Count outside of 1st round ranks
    dplyr::mutate(unranked = purrr::map(stan_id, ~length(which(old_unranked %>% select(num_range("Rank_", 33:602)) == .x)))) %>%
    tidyr::unnest(c(num1, top5, top32, unranked)) %>%
    # Take 
    dplyr::mutate(
      prop1 = (num1 + 2) / (num1 + top5 + top32 + unranked + 8),
      prop5 = (top5 + 2) / (num1 + top5 + top32 + unranked + 8),
      prop32 = (top32 + 2) / (num1 + top5 + top32 + unranked + 8),
      prop_ur = (unranked + 2) / (num1 + top5 + top32 + unranked + 8)
    ) %>%
    dplyr::mutate(score = 12 * prop1 + 6 * prop5 + 2 * prop32 + 0 * prop_ur) %>%
    dplyr::group_by(draft_year) %>%
    dplyr::mutate(score = score - mean(score)) %>%
    dplyr::mutate(prob = exp(score) / sum(exp(score))) %>%
    dplyr::ungroup() %>%
    dplyr::arrange(stan_id)
  
  # Remove the 2022 draft - we want to predict on this
  rankings_model_v4 = rankings_model_v3 %>%
    filter(resource_id != "2022_NHL_Draft")
  
  if (output_prior) {
    return(list(
      rankings = rankings_model_v4,
      agencies = agencies,
      prior = theta_prior
    ))
  } else {
    return(list(
      rankings = rankings_model_v4,
      agencies = agencies
    ))
  }
}