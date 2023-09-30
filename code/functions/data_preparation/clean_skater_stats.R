# Clean raw skater statistics data that were scraped from Elite Prospects
source("code/functions/data_preparation/league_region_finder.R")
source("code/functions/data_preparation/league_nation_finder.R")
source("code/functions/data_preparation/league_continent_finder.R")
source("code/functions/data_preparation/league_age_finder.R")

clean_skater_stats = function(skater_stats) {
  skater_stats_clean = skater_stats %>%
    dplyr::mutate(ep_id = as.numeric(ep_id)) %>%
    # Clean up tournament/league labels
    dplyr::mutate(event_type = case_when(
      league %in% c("WC", "WC D1A", "WC D1B", "OG", "OGQ") ~ "tournament",
      grepl("WJC", league) ~ "tournament",
      grepl("International", league) ~ "tournament",
      TRUE ~ event_type
    )) %>%
    # Clean up seasons
    dplyr::mutate(season = as.character(season)) %>%
    dplyr::mutate(season = dplyr::case_when(
      season == "01-Feb" ~ "2001-02",
      season == "02-Mar" ~ "2002-03",
      season == "03-Apr" ~ "2003-04",
      season == "04-May" ~ "2004-05",
      season == "05-Jun" ~ "2005-06",
      season == "06-Jul" ~ "2006-07",
      season == "07-Aug" ~ "2007-08",
      season == "08-Sep" ~ "2008-09",
      season == "09-Oct" ~ "2009-10",
      season == "10-Nov" ~ "2010-11",
      season == "11-Dec" ~ "2011-12",
      TRUE ~ season
    )) %>%
    dplyr::rowwise() %>%
    dplyr::mutate(season = ifelse(is.na(season), strsplit(league_url, "/")[[1]][7], season)) %>%
    dplyr::mutate(year_end = as.numeric(paste0(
      stringr::str_sub(season, start = 1, end = 2),
      stringr::str_sub(season, start = 6, end = 7)
    ))) %>%
    ungroup() %>%
    # Extract region, nation and continent of league
    dplyr::mutate(league_region = league_region_finder(league)) %>%
    dplyr::mutate(league_nation = league_nation_finder(league_region)) %>%
    dplyr::mutate(league_continent = league_continent_finder(league_nation)) %>%
    dplyr::mutate(league_age_class = league_age_finder(league)) %>%
    # Convert stats to numeric
    dplyr::mutate_if(
      names(.) %in% c("reg_gp", "reg_g", "reg_a", "reg_pts", "reg_pim", "reg_pm", "post_gp", "post_g", "post_a", "post_pts", "post_pim", "post_pm"),
      as.numeric
    ) %>%
    dplyr::mutate(reg_pts = reg_g + reg_a, post_pts = post_g + post_a) %>%
    # Select desired columns
    dplyr::select(
      ep_id, event_type, season, year_end, league_continent, league_nation, league_region, league_age_class,
      league_url, league, team, reg_gp, reg_g, reg_a, reg_pts, reg_pim, reg_pm, post_type, post_gp, post_g,
      post_a, post_pts, post_pim, post_pm, date_retrieved, source
    )
}