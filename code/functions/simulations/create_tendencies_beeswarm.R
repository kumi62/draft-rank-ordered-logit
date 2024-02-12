
create_tendencies_beeswarm = function(beta_heights_means, beta_propsr_means, beta_overage_means) {
  beta_means = beta_heights_means %>%
    mutate(type = "Height Tendency Parameter") %>%
    bind_rows(beta_overage_means %>% mutate(type = "Overage Tendency Parameter")) %>%
    bind_rows(beta_propsr_means %>% mutate(type = "Professional Experience Tendency Parameter")) %>%
    mutate(agency_name = case_when(
      agency_name == "Sportsnet - Sam Cosentino" ~ "SN-SC",
      agency_name == "TSN - Craig Button" ~ "TSN-CB",
      agency_name == "TSN - Bob McKenzie" ~ "TSN-BM",
      agency_name == "NHL Central Scouting - Full Staff" ~ "NHLCS",
      agency_name == "The Hockey News - Ryan Kennedy" ~ "THN-RK",
      agency_name == "Daily Faceoff - Chris Peters" ~ "DF-CP",
      agency_name == "Elite Prospects - Cam Robinson" ~ "EP-CR",
      agency_name == "Elite Prospects - Full Staff" ~ "EP",
      agency_name == "FC Hockey - Full Staff" ~ "FCH",
      agency_name == "The Athletic - Corey Pronman" ~ "TA-CP",
      agency_name == "The Athletic - Scott Wheeler" ~ "TA-SW",
      agency_name == "The Draft Analyst - Steve Kournianos" ~ "TDA-SK",
      agency_name == "The Hockey Writers - Matthew Zator" ~ "THW-MZ",
      agency_name == "The Hockey Writers - Peter Baracchini" ~ "THW-PB",
      agency_name == "The Hockey Writers - Andrew Forbes" ~ "THW-AF",
      agency_name == "Recruit Scouting - Full Staff" ~ "RS",
      agency_name == "Dobber Prospects - Full Staff" ~ "DP",
      agency_name == "McKeen's Hockey - Full Staff" ~ "MKH",
      agency_name == "Draft Prospects Hockey - Full Staff" ~ "DPH",
      agency_name == "Scouching - Will Scouch" ~ "SCO-WS",
      agency_name == "Smaht Scouting - Full Staff" ~ "SS",
      TRUE ~ agency_name
    )) %>%
    mutate(mean = ifelse(agency_name == "TDA-SK" & type == "Overage Tendency Parameter", -1.9, mean)) %>%
    mutate(agency_type = ifelse(agency_type == "resource", "Ranking Agency", "NHL Team"))
  
  group_means = beta_means %>%
    group_by(agency_type, type) %>%
    summarize(type_mean = mean(mean))
  
  tendencies_plot = beta_means %>%
    ggplot() +
    geom_hline(data = group_means, aes(yintercept = type_mean, colour = agency_type)) +
    geom_hline(aes(yintercept = 0), linetype = "longdash") +
    geom_label(aes(x = agency_type, y = mean, label = agency_name, fill = agency_type), size = 3.5, position = position_quasirandom(), alpha = 0.6) +
    theme_bw() +
    theme(legend.position = "none") +
    theme(axis.text = element_text(size = 20), axis.title = element_text(size = 20), strip.text = element_text(size = 20)) +
    facet_wrap(~type, ncol = 1) +
    labs(x = "Agency Type", y = "Posterior Mean of Tendency Parameter")
  
  return(tendencies_plot)
}