# Map league to the primary country it is in
league_nation_finder = function(region) {
  nation = case_when(
    region %in% c("Western Canada", "Quebec/Atlantic Canada", "Ontario", "Canada") ~ "CAN",
    region %in% c("USA") ~ "USA",
    region %in% c("Sweden") ~ "SWE",
    region %in% c("Finland") ~ "FIN",
    region %in% c("Russia") ~ "RUS",
    region %in% c("Czechia") ~ "CZE",
    region %in% c("Slovakia") ~ "SVK",
    region %in% c("Switzerland") ~ "SUI",
    region %in% c("Germany") ~ "GER",
    region %in% c("Latvia") ~ "LAT",
    region %in% c("Denmark") ~ "DEN",
    region %in% c("Norway") ~ "NOR",
    region %in% c("Austria") ~ "AUT",
    region %in% c("Belarus") ~ "BLR",
    region %in% c("Ukraine") ~ "UKR",
    region %in% c("Kazakhstan") ~ "KAZ",
    region %in% c("France") ~ "FRA",
    region %in% c("Italy") ~ "ITA",
    region %in% c("Slovenia") ~ "SLO",
    region %in% c("Great Britain") ~ "GBR",
    region %in% c("Estonia") ~ "EST",
    region %in% c("Hungary") ~ "HUN",
    region %in% c("Japan") ~ "JPN",
    region %in% c("China") ~ "CHN",
    region %in% c("Australia") ~ "AUS",
    region %in% c("New Zealand") ~ "NZL",
    TRUE ~ region
  )
  
  return(nation)
}