# Map league to particular age group
league_age_finder = function(league) {
  age_class = case_when(
    grepl("NCAA|USports", league) ~ "College",
    league %in% c("EUHL") ~ "College",
    
    grepl("U21|U20|U19|U18|U17|U16|U15|U14|U13|U12|J21|J20|J19|J18|J17|J16|J15|J14|J13|21U|20U|19U|18U|17U|16U|15U|14U|13U|Jr|Junior|Bantam|Midget", league) ~ "Junior",
    grepl("Mini|Novizen|Pucken|WJC|Hlinka|USHS|CAHS|AAA|MJAHL|GTHL|ALLIANCE|YOG|OJHL|MJHL|SJHL|BCHL|USPHL|QBAA|MetJHL|CCHL|AJHL|MMHL|SIJHL|UMHS|NCDC|DNL", league) ~ "Junior",
    league %in% c(
      "WHL", "OHL", "QMJHL", "USHL", "NAHL", "NA3HL", "MHL", "EBJL", "MHL B", "USDP", "NMHL",
      "DHL Cup", "DHL SuperCup", "EHL", "AMHL", "ICEJL", "ICEYSL", "CISAA", "MJAHL", "AMHL",
      "EHL", "CPSHA", "PIJHL", "MPHL", "EBYSL", "QMEAA"
    ) ~ "Junior",
    
    league %in% c(
      "NHL", "AHL", "ECHL", "SPHL", "FHL",
      "KHL", "VHL",
      "SHL", "HockeyAllsvenskan", "Allsvenskan", "HockeyEttan", "Division 2", "Division 3",
      "SM-liiga", "Liiga", "Mestis",
      "DEL", "DEL2", "Germany", "Germany2", "Germany3", "Germany4", "Germany5",
      "Belarus Vysshaya", "Belarus", "Belarus2",
      "Latvia", "Latvia2",
      "EIHL",
      "Kazakhstan",
      "Denmark", "Denmark2",
      "Slovakia", "Slovakia2", "Slovakia3", "Slovakia Q", 
      "China",
      "Norway", "Norway2",
      "Czech", "Czechia", "Czechia2", "Czechia3", "Czechia4", "Czechia Q",
      "AlpsHL", "EBEL", "ICEHL", "Austria", "Austria2",
      "NL", "SL", "NLA", "NLB", "MSL",
      "Ligue Magnus", 
      "Ukraine", 
      "Estonia",
      "Italy", "Italy2", "Italy3",
      "Slovenia", 
      "WC", "WC D1A", "WC D1B", "OG"
    ) ~ "Senior"
  )
  
  return(age_class)
}