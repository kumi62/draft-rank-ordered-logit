# Map nation to the continent it is in
league_continent_finder = function(nation) {
  continent = case_when(
    nation %in% c("CAN", "USA", "CAN/USA") ~ "North America",
    nation %in% c("JPN", "CHN") ~ "Asia",
    nation %in% c("AUS", "NZL") ~ "Oceania",
    !is.na(nation) ~ "Europe"
  )
  
  return(continent)
}