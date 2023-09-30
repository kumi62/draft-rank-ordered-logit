# Clean raw player information data that were scraped from Elite Prospects
clean_player_info = function(player_info) {
  player_info_clean = player_info %>%
    dplyr::mutate(ep_id = as.numeric(ep_id)) %>%
    # Convert height and weight to cm and kg numeric variables, respectively
    tidyr::separate(height, into = c("height_in", "height_cm"), sep = "/") %>%
    dplyr::mutate(height = height_cm %>% str_remove("cm") %>% trimws() %>% as.numeric()) %>%
    tidyr::separate(weight, into = c("weight_lbs", "weight_kg"), sep = "/") %>%
    dplyr::mutate(weight = weight_kg %>% str_remove("kg") %>% trimws() %>% as.numeric()) %>%
    # Extract the players' primary and secondary nation
    dplyr::rowwise() %>%
    dplyr::mutate(nation_primary = ifelse(grepl("/", nation), strsplit(nation, "/")[[1]][1] %>% trimws(), nation)) %>%
    dplyr::mutate(nation_secondary = ifelse(grepl("/", nation), strsplit(nation, "/")[[1]][2] %>% trimws(), NA)) %>%
    dplyr::ungroup() %>%
    dplyr::select(
      ep_id, birthdate, birthplace, nation_primary, nation_secondary,
      height, weight, pos, handedness, date_retrieved, source
    ) %>%
    # Replace "-" with NAs
    dplyr::mutate_if(names(.) %in% c("birthplace", "handedness", "pos"), ~ifelse(. == "-", NA, .))
  
  return(player_info_clean)
}