# Clean raw goalie statistics data that were scraped from Elite Prospects
source("code/functions/data_preparation/league_region_finder.R")
source("code/functions/data_preparation/league_nation_finder.R")
source("code/functions/data_preparation/league_continent_finder.R")
source("code/functions/data_preparation/league_age_finder.R")

clean_goalie_stats = function(goalie_stats) {
  goalie_stats_clean = goalie_stats %>%
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
      stringr::str_sub(season, start = 6, end = 7))
    )) %>%
    dplyr::ungroup() %>%
    # Extract region, nation and continent of league
    dplyr::mutate(league_region = league_region_finder(league)) %>%
    dplyr::mutate(league_nation = league_nation_finder(league_region)) %>%
    dplyr::mutate(league_continent = league_continent_finder(league_nation)) %>%
    dplyr::mutate(league_age_class = league_age_finder(league)) %>%
    # Clean up goalie records and TOI
    dplyr::mutate(
      reg_rec = reg_rec %>%
        stringr::str_replace("200", "0") %>%
        stringr::str_replace("201", "1") %>%
        stringr::str_replace("202", "2") %>%
        stringr::str_replace("193", "3") %>%
        stringr::str_replace("194", "4") %>%
        stringr::str_replace("195", "5") %>%
        stringr::str_replace("196", "6") %>%
        stringr::str_replace("197", "7") %>%
        stringr::str_replace("198", "8") %>%
        stringr::str_replace("199", "9"),
      post_rec = post_rec %>%
        stringr::str_replace("200", "0") %>%
        stringr::str_replace("201", "1") %>%
        stringr::str_replace("202", "2") %>%
        stringr::str_replace("193", "3") %>%
        stringr::str_replace("194", "4") %>%
        stringr::str_replace("195", "5") %>%
        stringr::str_replace("196", "6") %>%
        stringr::str_replace("197", "7") %>%
        stringr::str_replace("198", "8") %>%
        stringr::str_replace("199", "9"),
      reg_toi = stringr::str_replace_all(reg_toi, " ", ""),
      post_toi = stringr::str_replace_all(post_toi, " ", "")
    ) %>%
    tidyr::separate(reg_rec, c("reg_w", "reg_l", "reg_otl"), sep = "-", remove = FALSE) %>%
    tidyr::separate(post_rec, c("post_w", "post_l", "post_otl"), sep = "-", remove = FALSE) %>%
    # Convert stats to numeric
    dplyr::mutate_if(
      names(.) %in% c(
        "reg_gp", "reg_gd", "reg_gaa", "reg_svp", "reg_ga", "reg_svs", "reg_so", "reg_w", "reg_l", "reg_otl", "reg_toi",
        "post_gp", "post_gd", "post_gaa", "post_svp", "post_ga", "post_svs", "post_so", "post_w", "post_l", "post_otl", "post_toi"
      ),
      as.numeric
    ) %>%
    # Select desired columns
    dplyr::select(
      ep_id, event_type, season, year_end, league_continent, league_nation, league_region, league_age_class,
      league_url, league, team, reg_gp, reg_gd, reg_gaa, reg_svp, reg_ga, reg_svs, reg_so, reg_toi, reg_w,
      reg_l, reg_otl, post_type, post_gp, post_gd, post_gaa, post_svp, post_ga, post_svs, post_so, post_toi,
      post_w, post_l, post_otl, date_retrieved, source
    )
  
  return(goalie_stats_clean)
}