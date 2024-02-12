# Convert player names to IDs
agency2id = function(agencies, agency_data, year) {
  
  data.frame(agency_name = agencies) %>%
    left_join(agency_data, by = "agency_name") %>%
    select(agency_id) %>%
    unlist() %>%
    unname()
  
}