"""
This file contains three sample scrapers for 2022 NHL draft results and ranking
sets.

Each scouting site and media outlet requires a custom scraper in order to gather
the rankings on each page. Below we use the BeautifulSoup and selenium packages
from Python in order to scrape data from HockeyDB (observed draft results), TSN
(ranking sets) and NHL Central Scouting (ranking sets).
"""

#%% SETUP ----------------------------------------------------------------------

# Load packages
import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from unidecode import unidecode
import re

# Remove SettingWithCopyWarning when calling df.loc[index, colname]
pd.options.mode.chained_assignment = None

# Start webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())



#%% HOCKEY DB (NHL DRAFT RESULTS) ----------------------------------------------
# Scrape NHL draft results from 2019-2022

# Create data frame to store NHL draft results
hockeydb_df = pd.DataFrame()

# List the site name
site = "HockeyDB"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        "https://www.hockeydb.com/ihdb/draft/nhl2022e.html",
        "https://www.hockeydb.com/ihdb/draft/nhl2021e.html",
        "https://www.hockeydb.com/ihdb/draft/nhl2020e.html",
        "https://www.hockeydb.com/ihdb/draft/nhl2019e.html"
    ],
    "date":[
        "2022-07-07",
        "2021-07-23",
        "2020-10-06",
        "2019-06-21"
    ],
    "author":np.nan,
    "year":[
        2022,
        2021,
        2020,
        2019
    ],
    "set_type":"results",
    "organizer_type":"NHL"
})



# For each ranking set...
for i, row in resource_df.iterrows():
    
    # Retrieve information about the ranking set
    url = row["url"]
    date = row["date"]
    author = row["author"]
    year = row["year"]
    set_type = row["set_type"]
    organizer_type = row["organizer_type"]
    
    
    # Open link to rankings and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    
    # Retrieve results table
    data_table = soup.find("table", {"class":"sortable autostripe"}).find("tbody").find_all("tr")
    
    
    # For each row in the results table (ie each player)...
    for player_data in data_table:
        
        # If no data, then skip...
        if len(player_data.find_all("td")) == 0:
            continue
        
        # Extract data
        rank = player_data.find_all("td")[1].text.strip()
        player = player_data.find_all("td")[3].text.strip()
        position = player_data.find_all("td")[4].text.strip()
        team = player_data.find_all("td")[2].text.strip()
        
        # Store data in draft_df
        player_df = pd.DataFrame({
            "resource_site":[site], 
            "resource_staff":[author], 
            "resource_date":[date],
            "resource_url":[url], 
            "rank":[rank], 
            "player":[player],
            "position":[position],
            "team":[team],
            "year":[year],
            "set_type":[set_type],
            "organizer_type":[organizer_type],
            "retrieval_method":["scrape"],
            "league_subset":[np.nan],
            "region_subset":[np.nan],
            "position_subset":[np.nan]
        })
        
        hockeydb_df = pd.concat([hockeydb_df, player_df])
    


    

#%% TSN TABLE ------------------------------------------------------------------
# Scrape ranking sets in table format from the TSN website for the 2022 NHL draft

# Create data frame to store TSN ranking sets
tsn_df = pd.DataFrame()

# List the site name
site = "TSN"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        "https://www.tsn.ca/juraj-slafkovsky-shane-wright-bob-mckenzie-nhl-draft-ranking-1.1818585",
        "https://www.tsn.ca/shane-wright-nhl-draft-lottery-ranking-1.1797605",
        "https://www.tsn.ca/shane-wright-nhl-draft-craig-button-1.1744645",
        "https://www.tsn.ca/craig-s-list-shane-wright-leads-forward-heavy-top-10-1.1721827"
    ],
    "date":[
        "2022-06-28",
        "2022-05-10",
        "2022-01-12",
        "2021-11-16"
    ],
    "author":[
        "Bob McKenzie",
        "Craig Button",
        "Craig Button",
        "Craig Button"
    ],
    "year":[
        2022,
        2022,
        2022,
        2022
    ],
    "set_type":"rank",
    "organizer_type":"individual"
})



# For each ranking set...
for i, row in resource_df.iterrows():
    
    # Retrieve information about the ranking set
    url = row["url"]
    date = row["date"]
    author = row["author"]
    year = row["year"]
    set_type = row["set_type"]
    organizer_type = row["organizer_type"]
    
    
    # Open link to rankings and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    
    # Retrieve rankings table
    data_table = soup.find("table", {"class":"stats-table-scrollable article-table ng-scope kinetic-active ng-table"}).find("tbody").find_all("tr")
    
    
    # For each row in the rankings table (ie each player)...
    for rows in data_table:
        
        # Extract player data
        rank = rows.find_all("td")[0].text.strip().strip("T")
        player = rows.find_all("td")[1].text.strip()
        position = rows.find_all("td")[3].text.strip()
        
        
        # If the row has no player, then skip...
        if player == "":
            continue
        
    
        # Store data in draft_df
        player_df = pd.DataFrame({
            "resource_site":[site], 
            "resource_staff":[author], 
            "resource_date":[date],
            "resource_url":[url], 
            "rank":[rank], 
            "player":[player],
            "position":[position],
            "team":[np.nan],
            "year":[year],
            "set_type":[set_type],
            "organizer_type":[organizer_type],
            "retrieval_method":["scrape"],
            "league_subset":[np.nan],
            "region_subset":[np.nan],
            "position_subset":[np.nan]
        })
        
        tsn_df = pd.concat([tsn_df, player_df])
    




#%% SPORTSNET ------------------------------------------------------------------
# Scrape ranking sets from Sportnet for the 2022 NHL draft

# Create data frame to store TSN ranking sets
sportsnet_df = pd.DataFrame()

# List the site name
site = "Sportsnet"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        "https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-final-edition/",
        "https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-april-edition/",
        "https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-march-edition/",
        "https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-february-edition/",
        "https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-january-edition/",
        "https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-december-edition/",
        "https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-november-edition/",
        "https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-october-edition/"
    ],
    "date":[
        "2022-06-15",
        "2022-04-20",
        "2022-03-09",
        "2022-02-09",
        "2022-01-12",
        "2021-12-08",
        "2021-11-03",
        "2021-10-13"
    ],
    "author":[
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino"
    ],
    "year":[
        2022,
        2022,
        2022,
        2022,
        2022,
        2022,
        2022,
        2022
    ],
    "set_type":"rank",
    "organizer_type":"individual"
})


for i, row in resource_df.iterrows():
    
    # Retrieve information about the ranking set
    url = row["url"]
    date = row["date"]
    author = row["author"]
    year = row["year"]
    set_type = row["set_type"]
    organizer_type = row["organizer_type"]
    
    # Open link and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    
    
    # Find bolded text (corresponds to players)
    bolded_text = soup.find("div", {"class":"article-body-content col-xs-12 col-md-8 col-lg-9 no-padding"}).find_all("strong")
    
    # For each player...
    for player_text in bolded_text:
        
        # Extract text
        player_text = player_text.text
        
        # Fix errors
        player_text = player_text.replace("15 Alex Newhook", "15. Alex Newhook")
        
        # Remove blank spaces
        if player_text == " ":
            continue
        
        if player_text == "":
            continue
        
        # Remove honourable mentions
        if "MENTION" in player_text.upper():
            continue
        
        # Remove other oddities
        if "HTTPS" in player_text.upper():
            continue
        
        if player_text.strip()[0] not in ["1","2","3","4","5","6","7","8","9","0"]:
            continue
        
        # Remove brackets & content
        player_text = re.sub("[\(\[].*?[\)\]]", "", player_text)
        
        # Extract player information
        rank = player_text.split(".")[0].strip("*").strip()
        player_text = player_text.split(".")[1]
        player = player_text.split(",")[0].strip()
        position = player_text.split(",")[1].strip()
        
        # Store data in sportsnet_df
        player_df = pd.DataFrame({
            "resource_site":[site], 
            "resource_staff":[author], 
            "resource_date":[date],
            "resource_url":[url], 
            "rank":[rank], 
            "player":[player],
            "position":[position],
            "team":[np.nan],
            "year":[year],
            "set_type":[set_type],
            "organizer_type":[organizer_type],
            "retrieval_method":["scrape"],
            "league_subset":[np.nan],
            "region_subset":[np.nan],
            "position_subset":[np.nan]
        })
        
        sportsnet_df = pd.concat([sportsnet_df, player_df])




#%% DATA CLEANING --------------------------------------------------------------
# Do some final data cleaning prior to saving the scraped results as a csv

# Combine results of three sample scrapers
draft_df = pd.concat([hockeydb_df, tsn_df, sportsnet_df])

# Data cleaning
draft_df["player"] = draft_df["player"].apply(unidecode) # Remove accents
draft_df["player"] = draft_df["player"].str.replace(")", "").str.strip() # Clean up oddities and strip space in player names
draft_df["rank"] = draft_df["rank"].str.replace("*", "").str.replace("T-", "").str.replace("T", "").str.strip()
draft_df["team"] = draft_df["team"].replace(np.nan, "NA") # Replace NAs with "NA" for now
draft_df["team"] = draft_df["team"].str.split("(").str[0].str.strip() # Remove pick trades
draft_df["team"] = np.select( # Fix trade names
    [draft_df["team"].str.contains("Carolina|Hurricanes|CAR", na=False),
     draft_df["team"].str.contains("Columbus|Blue Jackets|CBJ", na=False),
     draft_df["team"].str.contains("New Jersey|Devils|NJ", na=False),
     draft_df["team"].str.contains("NY Islanders|Islanders|NYI", na=False),
     draft_df["team"].str.contains("NY Rangers|Rangers|NYR", na=False),
     draft_df["team"].str.contains("Philadelphia|Flyers|PHI", na=False),
     draft_df["team"].str.contains("Pittsburgh|Penguins|PIT", na=False),
     draft_df["team"].str.contains("Washington|Capitals|WSH", na=False),
     draft_df["team"].str.contains("Boston|Bruins|BOS", na=False),
     draft_df["team"].str.contains("Buffalo|Sabres|BUF", na=False),
     draft_df["team"].str.contains("Detroit|Red Wings|DET", na=False),
     draft_df["team"].str.contains("Florida|Panthers|FLA", na=False),
     draft_df["team"].str.contains("Montreal|Canadiens|MTL|MON", na=False),
     draft_df["team"].str.contains("Ottawa|Senators|OTT", na=False),
     draft_df["team"].str.contains("Tampa|Lightning|TB", na=False),
     draft_df["team"].str.contains("Toronto|Maple Leafs|TOR", na=False),
     draft_df["team"].str.contains("Arizona|Coyotes|ARI|ARZ", na=False),
     draft_df["team"].str.contains("Chicago|Blackhawks|CHI", na=False),
     draft_df["team"].str.contains("Colorado|Avalanche|COL", na=False),
     draft_df["team"].str.contains("Dallas|Stars|DAL", na=False),
     draft_df["team"].str.contains("Minnesota|Wild|MIN", na=False),
     draft_df["team"].str.contains("Nashville|Predators|NSH|NAS", na=False),
     draft_df["team"].str.contains("St Louis|St. Louis|Blues|STL", na=False),
     draft_df["team"].str.contains("Winnipeg|Jets|WPG|WIN", na=False),
     draft_df["team"].str.contains("Anaheim|Ducks|ANA", na=False),
     draft_df["team"].str.contains("Calgary|Flames|CGY|CAL", na=False),
     draft_df["team"].str.contains("Edmonton|Oilers|EDM", na=False),
     draft_df["team"].str.contains("Los Angeles|Kings|LA|Los-Angeles", na=False),
     draft_df["team"].str.contains("San Jose|Sharks|SJ", na=False),
     draft_df["team"].str.contains("Seattle|Kraken|SEA", na=False),
     draft_df["team"].str.contains("Vancouver|Canucks|VAN", na=False),
     draft_df["team"].str.contains("Vegas|Knights|VGK|VEG", na=False),
     True],
    ["CAR", "CBJ", "NJ", "NYI", "NYR", "PHI", "PIT", "WSH", "BOS", "BUF", "DET", "FLA", "MTL", "OTT", "TB", "TOR", 
     "ARI", "CHI", "COL", "DAL", "MIN", "NSH", "STL", "WPG", "ANA", "CGY", "EDM", "LA", "SJ", "SEA", "VAN", "VGK", draft_df["team"]]
    )
draft_df["team"] = draft_df["team"].replace("NA", np.nan) # Replace "NA" with NA for now
draft_df["position"] = draft_df["position"].astype(str).str.replace(" ", "") # Clean up player positions
draft_df["position"] = np.select( # Standardize player positions
    [draft_df["position"].str.upper().str.contains("CENT&LEFT WING", na=False) | draft_df["position"].str.upper().str.contains("C&LW", na=False),
     draft_df["position"].str.upper().str.contains("CENT&RIGHT WING", na=False) | draft_df["position"].str.upper().str.contains("C&RW", na=False),
     draft_df["position"].str.upper().str.contains("CENT&WING", na=False) | draft_df["position"].str.upper().str.contains("C&W", na=False),
     draft_df["position"].str.upper().str.contains("GOALIE|GOALTENDER", na=False),
     draft_df["position"].str.upper().str.contains("LEFT WING|LW", na=False),
     draft_df["position"].str.upper().str.contains("RIGHT WING|RW", na=False),
     draft_df["position"].str.upper().str.contains("WING|W", na=False),
     draft_df["position"].str.upper().str.contains("CENT|C", na=False),
     draft_df["position"].str.upper().str.contains("G", na=False),
     draft_df["position"].str.upper().str.contains("FORWARD|F", na=False),
     draft_df["position"].str.upper().str.contains("D", na=False),
     True],
    ["C/LW", "C/RW", "C/W", "G", "LW", "RW", "W", "C", "G", "F", "D", draft_df["position"]]
    )
draft_df["position"] = np.where(draft_df["position"] == "L", "LW", draft_df["position"])
draft_df["position"] = np.where(draft_df["position"] == "R", "RW", draft_df["position"])
draft_df["position"] = np.where(draft_df["position"] == "nan", np.nan, draft_df["position"]) # Replace "nan" with np.nan
draft_df = draft_df.reset_index(drop = True) # Reset the index


# Save the new data
draft_df.to_csv("data/rankings/sample_ranking_scrapers.csv", index = False)





