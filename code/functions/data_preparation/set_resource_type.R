# Define the resource type (i.e., scouting_service, draft_results, media, blog)
set_resource_type = function(resource_site) {
  resource_type = dplyr::case_when(
    resource_site == "HockeyDB" ~ "draft_results",
    resource_site %in% c("NHL Central Scouting", "Elite Prospects", "FC Hockey", "McKeen's Hockey", "Scouching", "Dobber Prospects",
                         "Smaht Scouting", "The Hockey Writers", "The Hockey News", "Recruit Scouting", "ISS Hockey", "The Draft Analyst",
                         "Draft Prospects Hockey", "Daily Faceoff") ~ "scouting_service",
    resource_site %in% c("TSN", "Sportsnet", "The Athletic", "ESPN") ~ "media",
    resource_site %in% c("Bleacher Report", "Fansided", "lines.com", "My NHL Draft", "SB Nation", "The Puck Authority", "NHL.com") ~ "blog"
  )
  
  resource_type = factor(resource_type, levels = c("draft_results", "scouting_service", "media", "blog"))
  
  return(resource_type)
}


