# Prepare player data to be integrated into model rankings data
source("code/functions/data_preparation/extract_dyear.R")
source("code/functions/data_preparation/extract_nation.R")
source("code/functions/data_preparation/extract_sr_proportion.R")
source("code/functions/data_preparation/extract_primary_league.R")
source("code/functions/data_preparation/extract_primary_region.R")
source("code/functions/data_preparation/extract_age_class.R")

prep_player_data_for_model = function(player_data_full, ranking_data_cleaned, years = c(2019, 2020, 2021, 2022)) {
  player_data_model = player_data_full %>%
    # Take only 2019 to 2022 drafts
    dplyr::filter(draft_year %in% years) %>%
    # Create nation of origin covariate
    dplyr::mutate(nation_origin = dplyr::case_when(
      nation_primary == "Canada" ~ "CAN",
      nation_primary == "USA" ~ "USA",
      nation_primary == "Sweden" ~ "SWE",
      nation_primary == "Finland" ~ "FIN",
      nation_primary == "Russia" ~ "RUS",
      TRUE ~ "EUR",
    )) %>%
    # Extract draft year league stats
    dplyr::mutate(dyear_league = purrr::map2(statistics, draft_year, extract_dyear)) %>%
    # Determine nation that a player is competing in during draft year
    dplyr::mutate(nation_compete = purrr::map(dyear_league, purrr::possibly(extract_nation, "DNP"))) %>%
    tidyr::unnest(nation_compete, keep_empty = TRUE) %>%
    dplyr::mutate(nation_compete = case_when(
      nation_compete %in% c("CAN", "USA", "SWE", "FIN", "RUS") ~ nation_compete,
      is.na(nation_compete) ~ "DNP",
      TRUE ~ "EUR"
    )) %>%
    # Determine weighted proportion of games at Sr level
    # mutate(age_class = future_map(dyear_league, extract_age_class)) %>%
    # unnest(age_class, keep_empty = TRUE) %>%
    dplyr::mutate(prop_sr = purrr::map(dyear_league, extract_sr_proportion)) %>%
    tidyr::unnest(prop_sr) %>%
    # Determine if a player is overaged, early birthdate or late birthdate for draft year
    dplyr::mutate(oa_date = paste0(draft_year - 19, "-09-16")) %>%
    dplyr::mutate(year_split_date = paste0(draft_year - 18, "-01-01")) %>%
    dplyr::mutate(age_split = case_when(
      as.Date(birthdate) < as.Date(oa_date) ~ "Overage",
      as.Date(birthdate) <= as.Date(year_split_date) ~ "Late",
      TRUE ~ "Early"
    )) %>%
    # Redefine position variable
    dplyr::mutate(pos_spec = dplyr::case_when(
      pos %in% c("LW/RW", "RW/LW", "RW", "LW", "W") ~ "W",
      grepl("/|F", pos) ~ "F",
      pos == "C" ~ "C",
      pos == "D" & handedness == "R" ~ "RHD",
      pos == "D" & handedness == "L" ~ "LHD",
      pos == "G" ~ "G"
    )) %>%
    dplyr::mutate(pos_broad = dplyr::case_when(
      pos_spec %in% c("C", "W", "F") ~ "F",
      pos_spec %in% c("RHD", "LHD") ~ "D",
      pos == "G" ~ "G"
    )) %>%
    # z-score height for each draft year and position
    dplyr::group_by(draft_year, pos_broad) %>%
    dplyr::mutate(height_z = (height - mean(height)) / sd(height)) %>%
    dplyr::ungroup() %>%
    # Determine primary league, region and continents
    dplyr::mutate(primary_league = purrr::map(dyear_league, purrr::possibly(extract_primary_league, "DNP"))) %>%
    dplyr::mutate(primary_region = purrr::map(dyear_league, purrr::possibly(extract_primary_region, "DNP"))) %>%
    dplyr::mutate(continents = purrr::map(dyear_league, purrr::possibly(~unique(.x$league_continent), "DNP"))) %>%
    # Clean up continents to match NHL Central Scouting for special cases
    dplyr::mutate(cont_count = purrr::map(continents, ~length(c(.x, "dummy")) - 1)) %>%
    tidyr::unnest(cont_count) %>%
    dplyr::mutate(continents = ifelse(cont_count != 1, NA, continents)) %>%
    tidyr::unnest(continents) %>%
    dplyr::mutate(continents = dplyr::case_when(
      player_id %in% c(
        "2015_201638", "2015_291003", "2015_579181", "2015_616308", "2015_718383", 
        "2016_236514", "2016_262138", "2016_629572", "2017_284917",
        "2018_247241", "2018_289453", "2018_335802", "2018_360966", "2019_292689",
        "2020_292067", "2020_388222", "2020_427906", "2021_293158", "2021_443711",
        "2021_472875", "2021_530466", "2021_541803", "2021_582502", "2022_535849",
        "2022_552041", "2022_602539"
      ) ~ "North America",
      player_id %in% c(
        "2016_687199", "2017_156953", "2017_687199", "2017_701870", 
        "2018_275725", "2018_395859", "2018_395860", "2021_596665",
        "2022_474745", "2022_527492"
      ) ~ "Europe",
      continents == "Europe" & nation_origin %in% c("CAN", "USA") & draft_year == 2021 ~ "North America",
      continents %in% c("Asia", "Oceania") ~ "Europe",
      TRUE ~ continents
    )) %>%
    # Create ID number for Stan model
    dplyr::semi_join(
      ranking_data_cleaned %>%
        dplyr::filter(year %in% years),
      by = c("player", "draft_year" = "year")
    ) %>%
    dplyr::arrange(player_id) %>%
    dplyr::ungroup() %>%
    dplyr::mutate(stan_id = dplyr::row_number()) %>%
    # Select relevant columns for model
    dplyr::select(
      stan_id, player_id, player, last_name, first_name, draft_year,
      pos_broad, pos_spec, primary_league, primary_region, continent = continents,
      nation_origin, nation_compete, prop_sr, height_z, age_split
    ) %>%
    tidyr::unnest(c(primary_league, primary_region))
}