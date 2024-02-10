
## STEP 0: LOAD PACKAGES AND FUNCTIONS -----------------------------------------

# Ensure the following packages are installed to run script
require(tidyverse)
require(fuzzyjoin)
require(janitor)
require(magrittr)

# Load required functions to run script
source("code/functions/data_preparation/clean_names.R")
source("code/functions/data_preparation/set_resource_type.R")
source("code/functions/data_preparation/set_resource_id.R")
source("code/functions/data_preparation/clean_player_info.R")
source("code/functions/data_preparation/clean_skater_stats.R")
source("code/functions/data_preparation/clean_goalie_stats.R")
source("code/functions/data_preparation/prep_player_data_for_model.R")
source("code/functions/data_preparation/restructure_ranking_data.R")
source("code/functions/data_preparation/convert_rankings_to_list.R")



## STEP 1: CLEAN RANKINGS DATA -------------------------------------------------

# Load raw, scraped ranking data
ranking_data = readr::read_csv(
  "data/rankings/ranking_data.csv",
  col_types = readr::cols(
    league_subset = readr::col_character(),
    region_subset = readr::col_character(),
    position_subset = readr::col_character(),
    nationality_subset = readr::col_character()
))

# Clean rankings data
ranking_data_cleaned = ranking_data %>%
  dplyr::filter(!is.na(rank) & rank != "HM") %>%
  dplyr::arrange(resource_date) %>%
  dplyr::mutate(rank = as.numeric(rank)) %>%
  dplyr::mutate(player = clean_names(player, year)) %>%
  dplyr::mutate(resource_type = set_resource_type(resource_site)) %>%
  dplyr::mutate(resource_id = set_resource_id(
    resource_site,
    year,
    resource_date,
    league_subset,
    region_subset,
    position_subset,
    nationality_subset
  )) %>%
  dplyr::select(resource_id, everything())

# Save as a csv
readr::write_csv(ranking_data_cleaned, "data/rankings/ranking_data_cleaned.csv")



## STEP 1a: [DATA CHECK] FIND PLAYERS NOT IN PLAYER DATA -----------------------

# Load data on all players to date
player_data = read_csv("data/players/player_data.csv")

# Find all new players in the newly scraped data
new_players = ranking_data_cleaned %>%
  dplyr::select(player, draft_year = year) %>%
  dplyr::distinct() %>%
  dplyr::anti_join(player_data %>% dplyr::select(player, draft_year))

if (nrow(new_players) > 0) {
  warning("There are unexpected players in the rankings that are not in `player_data.csv`")
}

# Add the new players to the players data frame
players = player_data %>%
  dplyr::bind_rows(new_players)

# MANUAL CHECK: 
#     Go through all the rows in new_players and check if they are actual new players or typos/different spellings
#     Fix all typos/different spellings by adjusting the clean_names function accordingly
#     Once all typos/different spellings are fixed, uncomment the first line below and save the new players to the player data frame
#     Use the "data_collection/update_player_data.py" file to obtain player information and statistics

# write.csv(players, "Data/players/player_data.csv", row.names = FALSE)



## STEP 1b: [DATA CHECK] CHECK FOR SIMILAR NAMES -------------------------------

# Use fuzzy matching to find all similar player names
player_matches = players %>%
  stringdist_join(
    players %>%
      dplyr::select(player_alt = player), by = c("player" = "player_alt"),
    mode = "left",
    method = "jw",
    max_dist = 0.15,
    distance_col = "similarity"
  ) %>%
  dplyr::filter(similarity != 0) %>%
  dplyr::mutate(similarity = round(similarity, 3)) %>%
  dplyr::select(player, player_alt, similarity) %>%
  dplyr::arrange(similarity)

# Load in all player names that we already know are similar
old_matches = read_csv("Data/players/similar_names.csv")

# Find the new similar player names (use this to fix player names in the clean_player_names function)
new_matches = player_matches %>%
  dplyr::anti_join(old_matches)

if (nrow(new_matches) > 0) {
  warning("There are potentially misspelled names in the rankings data, check `new_matches` and update accordingly.")
}

# MANUAL CHECK: 
#     Go through all matches and find typos/different spellings
#     Fix all typos/different spellings by adjusting the clean_names function accordingly
#     Once all typos/different spellings are fixed, uncomment the first line below and save the full data frame of player matches

# # Save all similar player names
# write.csv(player_matches, "Data/players/similar_names.csv", row.names = FALSE)



## STEP 2: CLEAN PLAYER INFORMATION AND STATISTICS -----------------------------

# Load player-specific information and statistics
player_info = read_csv("data/players/player_information.csv")
skater_stats = read_csv("data/players/skater_statistics.csv")
goalie_stats = read_csv("data/players/goalie_statistics.csv")

# Clean player-specific information and statistics
player_info_cleaned = clean_player_info(player_info)
skater_stats_cleaned = clean_skater_stats(skater_stats)
goalie_stats_cleaned = clean_goalie_stats(goalie_stats)

# Save cleaned statistics and player info
write_csv(player_info_cleaned, "data/players/player_information_cleaned.csv")
write_csv(skater_stats_cleaned, "data/players/skater_statistics_cleaned.csv")
write_csv(goalie_stats_cleaned, "data/players/goalie_statistics_cleaned.csv")

# Row bind skater and goalie statistics
statistics = skater_stats_cleaned %>%
  dplyr::bind_rows(goalie_stats_cleaned) %>%
  dplyr::select(-date_retrieved, -source)

# Join together player_data, player_information and statistics
player_data_full = players %>%
  mutate(ep_id = as.numeric(ep_id)) %>%
  left_join(player_info_cleaned, by = "ep_id") %>%
  nest_join(statistics, by = "ep_id")



## STEP 3: ADD PLAYER STATISTICS AND INFORMATION INTO RANKINGS TABLE -----------

# Refine the player data to only necessary data for modelling
player_data_model = prep_player_data_for_model(player_data_full, ranking_data_cleaned)

# Check: Are there any duplicates?
player_dupes = player_data_model %>%
  janitor::get_dupes("player_id")

if (nrow(player_dupes) > 0) {
  warning("There are duplicated player entries! This may cause issues with modelling.")
}

# Join player data to rankings
ranking_data_full = ranking_data_cleaned %>%
  dplyr::filter(year %in% c(2019, 2020, 2021, 2022)) %>%
  dplyr::left_join(player_data_model, dplyr::join_by(player, year == draft_year))

# Check that there are no NAs or doubles
if (nrow(ranking_data_full %>% dplyr::filter(is.na(stan_id))) > 0) {
  warning("Some players are listed as NA in rankings!")
}

if (nrow(ranking_data_full %>% dplyr::select(all_of(colnames(ranking_data_cleaned))) %>% janitor::get_dupes(resource_id, rank)) > 0) {
  warning("Some rankings are duplicated!")
}



## STEP 4: FORMAT DATA TO BE ABLE TO RUN MODEL ---------------------------------

# Restructure rankings data frame to be in similar format to model
ranking_data_model = restructure_ranking_data(ranking_data_full, player_data_model)

# Convert data frame into list that is compatible with our Stan models
ranking_data_list = convert_rankings_to_list(
  ranking_data_model$rankings,
  ranking_data_model$agencies,
  ranking_data_model$prior,
  player_data_model
)


# Also run for 2021 and 2022 individually
player_data_model_21 = prep_player_data_for_model(player_data_full, ranking_data_cleaned, years = c(2021))
ranking_data_full_21 = ranking_data_cleaned %>%
  dplyr::filter(year == 2021) %>%
  dplyr::left_join(player_data_model_21, dplyr::join_by(player, year == draft_year))
ranking_data_model_21 = restructure_ranking_data(ranking_data_full_21, player_data_model_21)
ranking_data_list_21 = convert_rankings_to_list(
  ranking_data_model_21$rankings,
  ranking_data_model_21$agencies,
  ranking_data_model_21$prior,
  player_data_model_21
)

player_data_model_22 = prep_player_data_for_model(player_data_full, ranking_data_cleaned, years = c(2022))
ranking_data_full_22 = ranking_data_cleaned %>%
  dplyr::filter(year == 2022) %>%
  dplyr::left_join(player_data_model_22, dplyr::join_by(player, year == draft_year))
ranking_data_model_22 = restructure_ranking_data(ranking_data_full_22, player_data_model_22)
ranking_data_list_22 = convert_rankings_to_list(
  ranking_data_model_22$rankings,
  ranking_data_model_22$agencies,
  ranking_data_model_22$prior,
  player_data_model_22
)



## STEP 5: STORE OUTPUTS -------------------------------------------------------

# Save player data and Stan data for modelling multiple drafts
write_csv(player_data_model, "data/model_input/model_player_data.csv")
write_rds(ranking_data_model$rankings, "data/model_input/model_rankings_data.Rda")
write_csv(ranking_data_model$agencies, "data/model_input/model_agencies_data.csv")
write_rds(ranking_data_list, "data/model_input/model_data_list.Rda")

# Save player data and Stan data for modelling 2021 draft
write_csv(player_data_model_21, "data/model_input/model_player_data_2021.csv")
write_rds(ranking_data_model_21$rankings, "data/model_input/model_rankings_data_2021.Rda")
write_csv(ranking_data_model_21$agencies, "data/model_input/model_agencies_data_2021.csv")
write_rds(ranking_data_list_21, "data/model_input/model_data_list_2021.Rda")

# Save player data and Stan data for modelling 2022 draft
write_csv(player_data_model_22, "data/model_input/model_player_data_2022.csv")
write_rds(ranking_data_model_22$rankings, "data/model_input/model_rankings_data_2022.Rda")
write_csv(ranking_data_model_22$agencies, "data/model_input/model_agencies_data_2022.csv")
write_rds(ranking_data_list_22, "data/model_input/model_data_list_2022.Rda")

