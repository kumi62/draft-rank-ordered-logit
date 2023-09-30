# Extract league statistics in draft year
extract_dyear = function(data, year, type = "league") {
  data %>%
    dplyr::filter(year_end == year & event_type == type)
}