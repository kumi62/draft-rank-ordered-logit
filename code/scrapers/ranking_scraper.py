"""
Created on Thu May 12 20:48:36 2022

@author: brendankumagai
"""


#%% LOAD PACKAGES AND DATA

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

# Set directory
os.chdir("/Users/brendankumagai/Sports-Analytics/2022-02_Plackett_Luce_Draft_Model")

# Remove SettingWithCopyWarning when calling df.loc[index, colname]
pd.options.mode.chained_assignment = None

# Start webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())



#%% RESET DATA FRAME TO TEMPORARILY STORE DRAFT RANKINGS

draft_df = pd.DataFrame()



#%% TRUE NHL DRAFT RESULTS

# List the site name
site = "HockeyDB"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        "https://www.hockeydb.com/ihdb/draft/nhl2022e.html",
        # "https://www.hockeydb.com/ihdb/draft/nhl2021e.html",
        # "https://www.hockeydb.com/ihdb/draft/nhl2020e.html",
        # "https://www.hockeydb.com/ihdb/draft/nhl2019e.html",
        # "https://www.hockeydb.com/ihdb/draft/nhl2018e.html",
        # "https://www.hockeydb.com/ihdb/draft/nhl2017e.html",
        # "https://www.hockeydb.com/ihdb/draft/nhl2016e.html",
        # "https://www.hockeydb.com/ihdb/draft/nhl2015e.html"
    ],
    "date":[
        "2022-07-07",
        # "2021-07-23",
        # "2020-10-06",
        # "2019-06-21",
        # "2018-06-22",
        # "2017-06-23",
        # "2016-06-24",
        # "2015-06-26"
    ],
    "author":np.nan,
    "year":[
        2022,
        # 2021,
        # 2020,
        # 2019,
        # 2018,
        # 2017,
        # 2016,
        # 2015
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
        
        draft_df = pd.concat([draft_df, player_df])
    


    

#%% TSN TABLE

# List the site name
site = "TSN"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2022 Draft
        #"https://www.tsn.ca/juraj-slafkovsky-shane-wright-bob-mckenzie-nhl-draft-ranking-1.1818585",
        #"https://www.tsn.ca/shane-wright-nhl-draft-lottery-ranking-1.1797605",
        #"https://www.tsn.ca/shane-wright-nhl-draft-craig-button-1.1744645",
        #"https://www.tsn.ca/craig-s-list-shane-wright-leads-forward-heavy-top-10-1.1721827",
        ## 2021 Draft
        #"https://www.tsn.ca/owen-power-the-unanimous-no-1-in-tsn-s-mid-season-draft-rankings-1.1626057",
        #"https://www.tsn.ca/craig-s-list-defencemen-dominate-top-of-nhl-draft-prospect-rankings-1.1638404",
        #"https://www.tsn.ca/craig-button-list-owen-power-nhl-draft-1.1666944",
        #"https://www.tsn.ca/defencemen-dominate-craig-button-s-early-look-at-2021-nhl-draft-class-1.1394203",
        ## 2020 Draft
        #"https://www.tsn.ca/craig-s-list-jamie-drysdale-yaroslav-askarov-move-up-in-final-edition-1.1534550",
        #"https://www.tsn.ca/bob-mckenzie-s-final-ranking-lafreniere-the-surest-thing-in-most-uncertain-draft-year-1.1488272",
        #"https://www.tsn.ca/craig-s-list-alexis-lafreniere-solidifies-status-as-hockey-s-top-prospect-1.1461675",
        #"https://www.tsn.ca/craig-button-s-list-canadian-forwards-dominate-top-of-first-nhl-draft-rankings-1.1363362",
        ## 2019 Draft
        #"https://www.tsn.ca/americans-set-to-dominate-first-round-of-the-nhl-draft-1.1323878",
        #"https://www.tsn.ca/craig-s-list-caufield-scores-his-way-into-top-5-1.1316942",
        #"https://www.tsn.ca/craig-s-list-hughes-leads-class-heavy-on-american-talent-1.1279391",
        ## 2018 Draft
        #"https://www.tsn.ca/kc-1.1115400",
        #"https://www.tsn.ca/craig-s-list-svechnikov-solidifies-hold-on-second-spot-1.1103996",
        ## 2017 Draft
        #"https://www.tsn.ca/mckenzie-s-draft-ranking-top-93-and-honourable-mentions-1.778987/kchow-template-100-1.778987",
        #"https://www.tsn.ca/craig-s-list-final-ranking-1.294692",
        ## 2016 Draft
        "https://www.tsn.ca/matthews-goes-wire-to-wire-as-tsn-s-top-prospect-1.511597",
        "https://www.tsn.ca/craig-s-list-matthews-no-1-because-position-matters-1.503562",
        "https://www.tsn.ca/tsn-mid-season-draft-ranking-topped-by-big-three-1.435206",
        ## 2015 Draft
        "https://www.tsn.ca/mckenzie-s-final-ranking-mcdavid-eichel-and-1.300634",
        "https://www.tsn.ca/craig-s-list-suspenseful-race-for-no-3-1.249965",
        "https://www.tsn.ca/craig-s-list-2015-mcdaivid-on-top-provorov-leaps-into-top-5-1.204945"
    ],
    "date":[
        ## 2022 Draft
        #"2022-06-28",
        #"2022-05-10",
        #"2022-01-12",
        #"2021-11-16",
        ## 2021 Draft
        #"2021-04-19",
        #"2021-05-12",
        #"2021-07-12",
        #"2020-11-07",
        ## 2020 Draft
        #"2020-10-05",
        #"2020-06-22",
        #"2020-03-30",
        #"2019-09-10",
        ## 2019 Draft
        #"2019-06-17",
        #"2019-06-06",
        #"2019-03-25",
        ## 2018 Draft
        #"2018-06-18",
        #"2018-06-05",
        ## 2017 Draft
        #"2017-06-19",
        #"2017-06-07",
        ## 2016 Draft
        "2016-06-20",
        "2016-06-08",
        "2016-02-08",
        ## 2015 Draft
        "2015-06-05",
        "2015-04-07",
        "2015-01-07"
    ],
    "author":[
        ## 2022 Draft
        #"Bob McKenzie",
        #"Craig Button",
        #"Craig Button",
        #"Craig Button",
        ## 2021 Draft
        #"Bob McKenzie",
        #"Craig Button",
        #"Craig Button",
        #"Craig Button",
        ## 2020 Draft
        #"Craig Button",
        #"Bob McKenzie",
        #"Craig Button",
        #"Craig Button",
        ## 2019 Draft
        #"Bob McKenzie",
        #"Craig Button",
        #"Craig Button",
        ## 2018 Draft
        #"Bob McKenzie",
        #"Craig Button",
        ## 2017 Draft
        #"Bob McKenzie",
        #"Craig Button",
        ## 2016 Draft
        "Bob McKenzie",
        "Craig Button",
        "Bob McKenzie",
        ## 2015 Draft
        "Bob McKenzie",
        "Craig Button",
        "Craig Button"
    ],
    "year":[
        ## 2022 Draft
        #2022,
        #2022,
        #2022,
        #2022,
        ## 2021 Draft
        #2021,
        #2021,
        #2021,
        #2021,
        ## 2020 Draft
        #2020,
        #2020,
        #2020,
        #2020,
        ## 2019 Draft
        #2019,
        #2019,
        #2019,
        ## 2018 Draft
        #2018,
        #2018,
        ## 2017 Draft
        #2017,
        #2017,
        ## 2016 Draft
        2016,
        2016,
        2016,
        ## 2015 Draft
        2015,
        2015,
        2015
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
        
        draft_df = pd.concat([draft_df, player_df])
    


#%% TSN HEADERS

# List the site name
site = "TSN"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2020 Draft
        #"https://www.tsn.ca/lafreniere-leads-loaded-class-in-tsn-hockey-s-pre-season-draft-ranking-1.1364438",
        ## 2019 Draft
        #"https://www.tsn.ca/craig-s-list-caufield-scores-his-way-into-top-5-1.1316942",
        "https://www.tsn.ca/hughes-kakko-in-tight-race-for-top-spot-1.1284470",
        "https://www.tsn.ca/hughes-leads-the-pack-in-tsn-hockey-s-pre-season-draft-ranking-1.1172382",
        ## 2018 Draft
        "https://www.tsn.ca/the-big-four-solidify-spots-in-tsn-draft-ranking-1.1066345",
        "https://www.tsn.ca/mckenzie-s-preseason-ranking-the-year-of-swedish-defencemen-1.852963",
        ## 2017 Draft
        "https://www.tsn.ca/mckenzie-s-pre-season-ranking-the-nolan-patrick-draft-1.567410",
        ## 2016 Draft
        "https://www.tsn.ca/laine-closes-gap-on-matthews-atop-tsn-draft-rankings-1.478128",
        "https://www.tsn.ca/elite-prospect-matthews-tops-mckenzie-s-ranking-1.364099",
        ## 2015 Draft
        "https://www.tsn.ca/2014-15-nhl-pre-season-draft-rankings-1.93188"
    ],
    "date":[
        ## 2020 Draft
        #"2019-09-16",
        ## 2019 Draft
        #"2019-06-06",
        "2019-04-04",
        "2018-09-17",
        ## 2018 Draft
        "2018-04-27",
        "2017-09-13",
        ## 2017 Draft
        "2016-09-22",
        ## 2016 Draft
        "2016-04-27",
        "2015-09-24",
        ## 2015 Draft
        "2014-09-25"
    ],
    "author":[
        ## 2020 Draft
        #"Bob McKenzie",
        ## 2019 Draft
        #"Craig Button",
        "Bob McKenzie",
        "Bob McKenzie",
        ## 2018 Draft
        "Bob McKenzie",
        "Bob McKenzie",
        ## 2017 Draft
        "Bob McKenzie",
        ## 2016 Draft
        "Bob McKenzie",
        "Bob McKenzie",
        ## 2015 Draft
        "Bob McKenzie"
    ],
    "year":[
        ## 2020 Draft
        #2020,
        ## 2019 Draft
        #2019,
        2019,
        2019,
        ## 2018 Draft
        2018,
        2018,
        ## 2017 Draft
        2017,
        ## 2016 Draft
        2016,
        2016,
        ## 2015 Draft
        2015
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
    headers = soup.find_all("div", {"class":"ranking-content"})
    
    
    # For each row in the rankings table (ie each player)...
    for header in headers:
        
        # Extract player data
        rank = header.find("h5").text.split(".")[0].strip()
        player = header.find("h5").text.split(".")[1].strip()
        position = header.find("p").text.split("|")[0].strip()
        
        # Remove brackets & content
        player = re.sub("[\(\[].*?[\)\]]", "", player)
        
        
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
        
        draft_df = pd.concat([draft_df, player_df])




#%% SPORTSNET

# List the site name
site = "Sportsnet"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2022 Draft
        #"https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-final-edition/",
        ##"https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-april-edition/",
        ##"https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-march-edition/",
        #"https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-february-edition/",
        #"https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-january-edition/",
        #"https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-december-edition/",
        #"https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-november-edition/",
        #"https://www.sportsnet.ca/nhl/article/sportsnets-2022-nhl-draft-prospect-rankings-october-edition/",
        ## 2020 Draft
        #"https://www.sportsnet.ca/nhl/article/sportsnets-2020-nhl-draft-prospect-rankings-final-edition/",
        #"https://www.sportsnet.ca/hockey/nhl/sportsnets-2020-nhl-draft-prospect-rankings-lottery-edition/",
        #"https://www.sportsnet.ca/hockey/nhl/sportsnets-2020-nhl-draft-prospect-rankings-april/",
        #"https://www.sportsnet.ca/hockey/nhl/sportsnets-2020-nhl-draft-prospect-rankings-march/",
        #"https://www.sportsnet.ca/hockey/nhl/sportsnets-2020-nhl-draft-prospect-rankings-february/",
        #"https://www.sportsnet.ca/hockey/nhl/sportsnets-2020-nhl-draft-prospect-rankings-january/",
        #"https://www.sportsnet.ca/hockey/nhl/sportsnets-2020-nhl-draft-prospect-rankings-december/",
        #"https://www.sportsnet.ca/hockey/juniors/sportsnets-2020-nhl-draft-prospect-rankings-november/",
        #"https://www.sportsnet.ca/hockey/nhl/sportsnets-2020-nhl-draft-prospect-rankings-october/",
        ## 2019 Draft
        "https://www.sportsnet.ca/hockey/nhl/sportsnets-2019-nhl-draft-prospect-rankings-may/",
        "https://www.sportsnet.ca/hockey/nhl/sportsnets-2019-nhl-draft-prospect-rankings-april/",
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-2019-nhl-draft-prospect-rankings-march/",
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-2019-nhl-draft-prospect-rankings-february/",
        "https://www.sportsnet.ca/hockey/nhl/sportsnets-2019-nhl-draft-prospect-rankings-january/",
        "https://www.sportsnet.ca/hockey/nhl/sportsnets-2019-nhl-draft-prospect-rankings-december/",
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-2019-nhl-draft-prospect-rankings-november/",
        "https://www.sportsnet.ca/hockey/nhl/sportsnets-2019-nhl-draft-prospect-rankings-october/",
        ## 2018 Draft
        "https://www.sportsnet.ca/hockey/nhl/sportsnets-2018-nhl-draft-prospect-rankings-lottery-edition/",
        "https://www.sportsnet.ca/hockey/nhl/sportsnets-2018-nhl-draft-prospect-rankings-march/",
        "https://www.sportsnet.ca/hockey/nhl/sportsnets-2018-nhl-draft-prospect-rankings-february/",
        #"https://www.sportsnet.ca/hockey/nhl/sportsnets-2018-nhl-draft-prospect-rankings-january/",
        "https://www.sportsnet.ca/hockey/nhl/sportsnets-2018-nhl-draft-prospect-rankings-december/",
        "https://www.sportsnet.ca/hockey/nhl/sportsnets-2018-nhl-draft-prospect-rankings-november/",
        "https://www.sportsnet.ca/hockey/nhl/sportsnets-2018-nhl-draft-prospect-rankings/",
        ## 2017 Draft
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-2017-nhl-draft-prospect-rankings-march/",
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-2017-nhl-draft-prospect-rankings-january/",
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-2017-nhl-draft-prospect-rankings-december/",
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-2017-nhl-draft-prospect-rankings-november/",
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-2017-nhl-draft-prospect-rankings-october-jeff-marek/",
        ## 2016 Draft
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-final-top-30-2016-nhl-draft-prospects/",
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-top-30-2016-nhl-draft-prospects-january/",
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-top-30-2016-nhl-draft-prospects-december/",
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-top-30-2016-nhl-draft-prospects-november-2015/",
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-top-30-2016-nhl-draft-prospects/",
        ## 2015 Draft
        "https://www.sportsnet.ca/hockey/juniors/sportsnets-top-30-nhl-draft-prospects/",
        "https://www.sportsnet.ca/hockey/juniors/top-30-nhl-draft-prospects-march/",
        "https://www.sportsnet.ca/hockey/juniors/top-30-nhl-draft-prospects-january/",
        "https://www.sportsnet.ca/hockey/nhl/top-30-nhl-draft-prospects-list/"
    ],
    "date":[
        ## 2022 Draft
        #"2022-06-15",
        ##"2022-04-20",
        ##"2022-03-09",
        #"2022-02-09",
        #"2022-01-12",
        #"2021-12-08",
        #"2021-11-03",
        #"2021-10-13",
        ## 2020 Draft
        #"2020-10-01",
        #"2020-06-25",
        #"2020-04-08",
        #"2020-03-04",
        #"2020-02-05",
        #"2020-01-08",
        #"2019-12-04",
        #"2019-11-06",
        #"2019-10-02",
        ## 2019 Draft
        "2019-05-08",
        "2019-04-09",
        "2019-03-13",
        "2019-02-13",
        "2019-01-09",
        "2018-12-12",
        "2018-11-07",
        "2018-10-02",
        ## 2018 Draft
        "2018-04-28",
        "2018-03-07",
        "2018-02-07",
        #"2018-01-10",
        "2017-12-06",
        "2017-11-01",
        "2017-10-03",
        ## 2017 Draft
        "2017-03-08",
        "2017-01-10",
        "2016-12-07",
        "2016-11-02",
        "2016-10-04",
        ## 2016 Draft
        "2016-05-20",
        "2016-01-13",
        "2015-12-17",
        "2015-11-18",
        "2015-10-14",
        ## 2015 Draft
        "2015-06-01",
        "2015-03-18",
        "2015-01-14",
        "2014-11-19"
    ],
    "author":[
        ## 2022 Draft
        #"Sam Cosentino",
        ##"Sam Cosentino",
        ##"Sam Cosentino",
        #"Sam Cosentino",
        #"Sam Cosentino",
        #"Sam Cosentino",
        #"Sam Cosentino",
        #"Sam Cosentino",
        ## 2020 Draft
        #"Sam Cosentino",
        #"Sam Cosentino",
        #"Sam Cosentino",
        #"Sam Cosentino",
        #"Sam Cosentino",
        #"Sam Cosentino",
        #"Sam Cosentino",
        #"Sam Cosentino",
        #"Sam Cosentino",
        ## 2019 Draft
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino",
        "Sam Cosentino",
        ## 2018 Draft
        "Jeff Marek",
        "Jeff Marek",
        "Jeff Marek",
        #"Jeff Marek",
        "Jeff Marek",
        "Jeff Marek",
        "Jeff Marek",
        ## 2017 Draft
        "Jeff Marek",
        "Jeff Marek",
        "Jeff Marek",
        "Jeff Marek",
        "Jeff Marek",
        ## 2016 Draft
        "Damien Cox",
        "Damien Cox",
        "Damien Cox",
        "Damien Cox",
        "Damien Cox",
        ## 2015 Draft
        "Damien Cox",
        "Damien Cox",
        "Damien Cox",
        "Damien Cox"
    ],
    "year":[
        ## 2022 Draft
        #2022,
        ##2022,
        ##2022,
        #2022,
        #2022,
        #2022,
        #2022,
        #2022,
        ## 2020 Draft
        #2020,
        #2020,
        #2020,
        #2020,
        #2020,
        #2020,
        #2020,
        #2020,
        #2020,
        ## 2019 Draft
        2019,
        2019,
        2019,
        2019,
        2019,
        2019,
        2019,
        2019,
        ## 2018 Draft
        2018,
        2018,
        2018,
        #2018,
        2018,
        2018,
        2018,
        ## 2017 Draft
        2017,
        2017,
        2017,
        2017,
        2017,
        ## 2016 Draft
        2016,
        2016,
        2016,
        2016,
        2016,
        ## 2015 Draft
        2015,
        2015,
        2015,
        2015
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
        
        draft_df = pd.concat([draft_df, player_df])





#%% NHL CENTRAL SCOUTING

# List the site name
site = "NHL Central Scouting"
author = "Full Staff"
set_type = "rank"
organizer_type = "individual"



years = [2015, 2016, 2017, 2018, 2019, 2020]
years = [2021]

terms = ["midterm", "final"]
terms = ["midterm"]

cats = [1,2,3,4]

# For each year, term and category...
for year in years:
    for term in terms:
        for cat in cats:
            
            # Open first page of rankings
            url1 = "http://www.nhl.com/ice/draftprospectbrowse.htm?cat=" + str(cat) + "&sort=" + term + "Rank&year=" + str(year) + "&pg=1"
            driver.get(url1)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, "lxml")
            
            # Scrape page numbers
            page_code = soup.find("div", {"class":"page-select-container"}).find_all("a")
            
            # Extract page numbers
            page_nums = ["1"]
            for element in page_code:
                element_text = element.text
                if  element_text in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    page_nums.append(element.text)
            
            # For each page...
            for page in page_nums:
                
                # Open first page of rankings
                url = "http://www.nhl.com/ice/draftprospectbrowse.htm?cat=" + str(cat) + "&sort=" + term + "Rank&year=" + str(year) + "&pg=" + page
                driver.get(url)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                
                # Extract table data
                data_table = soup.find("table", {"class":"stat-table"}).find("tbody").find_all("tr")
                
                # For each row...
                for row in data_table:
                    
                    if len(row.find_all("td")) == 1:
                        continue
                    
                    if term == "final":
                        rank = row.find_all("td")[0].text.strip()
                    if term == "midterm":
                        rank = row.find_all("td")[1].text.strip()
                    last = row.find_all("td")[2].text.strip().split(",")[0].strip()
                    first = row.find_all("td")[2].text.strip().split(",")[1].strip()
                    player = (first + " " + last).title()
                    position = row.find_all("td")[5].text.strip()
                    
                    if rank == "":
                        continue
            
                    if int(rank) > 900:
                        continue
                    
                    if cat == 1:
                        region_subset = "North America"
                        position_subset = "Skaters"
                    elif cat == 2:
                        region_subset = "Europe"
                        position_subset = "Skaters"
                    elif cat == 3:
                        region_subset = "North America"
                        position_subset = "Goalies"
                    elif cat == 4:
                        region_subset = "Europe"
                        position_subset = "Goalies"
                        
                    
                    # Store data in draft_df
                    player_df = pd.DataFrame({
                        "resource_site":[site], 
                        "resource_staff":[author], 
                        "resource_date":[np.nan],
                        "resource_url":[url1], 
                        "rank":[rank], 
                        "player":[player],
                        "position":[position],
                        "team":[np.nan],
                        "year":[year],
                        "set_type":[set_type],
                        "organizer_type":[organizer_type],
                        "retrieval_method":["scrape"],
                        "league_subset":[np.nan],
                        "region_subset":[region_subset],
                        "position_subset":[position_subset]
                    })
                    
                    draft_df = pd.concat([draft_df, player_df])




#%% THE HOCKEY WRITERS

# List the site name
site = "The Hockey Writers"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2023 Draft
        ## "https://thehockeywriters.com/2023-nhl-draft-rankings-forbes-top-16/",
        ## "https://thehockeywriters.com/2023-nhl-draft-rankings-early-top-15-baracchini/",
        ## 2022 Draft
        # "https://thehockeywriters.com/2022-nhl-draft-rankings-final-july-zator/",
        #"https://thehockeywriters.com/2022-nhl-draft-rankings-final-june-baracchini/",
        #"https://thehockeywriters.com/2022-nhl-draft-rankings-april-zator/",
        #"https://thehockeywriters.com/2022-nhl-draft-rankings-february-zator/",
        #"https://thehockeywriters.com/2022-nhl-draft-rankings-may-baracchini/",
        #"https://thehockeywriters.com/2022-nhl-draft-rankings-march-baracchini/",
        #"https://thehockeywriters.com/2022-nhl-draft-rankings-december-baracchini/",
        ##"https://thehockeywriters.com/2022-nhl-draft-rankings-preseason-baracchini/", # Can't scrape
        #"https://thehockeywriters.com/2022-nhl-draft-rankings-march-forbes/",
        ##"https://thehockeywriters.com/2022-nhl-draft-rankings-january-forbes/", # Can't scrape
        ## 2021 Draft
        #"https://thehockeywriters.com/2021-nhl-draft-final-rankings-zator/",
        #"https://thehockeywriters.com/2021-nhl-draft-rankings-zator-april/",
        #"https://thehockeywriters.com/2021-nhl-draft-rankings-february-zator/",
        #"https://thehockeywriters.com/2021-nhl-draft-rankings-baracchini-final-rankings/",
        #"https://thehockeywriters.com/2021-nhl-draft-rankings-baracchini-top-100-march/",
        #"https://thehockeywriters.com/2021-nhl-draft-rankings-baracchini-top-75-january/",
        #"https://thehockeywriters.com/2021-nhl-draft-rankings-forbes-final-160/",
        #"https://thehockeywriters.com/2021-nhl-draft-rankings-forbes-may/",
        #"https://thehockeywriters.com/2021-nhl-draft-rankings-forbes-february/"
    ],
    "date":[
        # # 2023 Draft
        ## "2022-08-07",
        ## "2022-07-29",
        ## 2022 Draft
        # "2022-07-02",
        #"2022-06-28",
        #"2022-04-05",
        #"2022-02-11",
        #"2022-05-07",
        #"2022-03-12",
        #"2022-12-09",
        ##"2021-09-13",
        #"2022-03-22",
        ##"2022-01-01",
        ## 2021 Draft
        #"2021-06-23",
        #"2021-04-03",
        #"2021-02-06",
        #"2021-06-09",
        #"2021-03-10",
        #"2021-01-20",
        #"2021-07-23",
        #"2021-05-15",
        #"2021-02-14"
    ],
    "author":[
        # # 2023 Draft
        ## "Andrew Forbes",
        ## "Peter Baracchini",
        # # 2022 Draft
        # "Matthew Zator",
        #"Peter Baracchini",
        #"Matthew Zator",
        #"Matthew Zator",
        #"Peter Baracchini",
        #"Peter Baracchini",
        #"Peter Baracchini",
        ##"Peter Baracchini",
        #"Andrew Forbes",
        ##"Andrew Forbes",
        # # 2021 Draft
        #"Matthew Zator",
        #"Matthew Zator",
        #"Matthew Zator",
        #"Peter Baracchini",
        #"Peter Baracchini",
        #"Peter Baracchini",
        #"Andrew Forbes",
        #"Andrew Forbes",
        #"Andrew Forbes"
    ],
    "year":[
        # # 2023 Draft
        ## 2023,
        ## 2023,
        # # 2022 Draft
        # 2022,
        #2022,
        # 2022,
        # 2022,
        # 2022,
        # 2022,
        # 2022,
        # #2022,
        # 2022,
        # #2022,
        # # 2021 Draft
        # 2021,
        # 2021,
        # 2021,
        # 2021,
        # 2021,
        # 2021,
        # 2021,
        # 2021,
        # 2021
    ],
    "set_type":"rank",
    "organizer_type":"individual"
})

# Baracchini, 2022 Preseason and Forbes, 2022 January manually scraped because of different formatting in source code



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
    
    
    # Retrieve all paragraphs in the article body
    paragraphs = soup.find("div", {"class":"entry-content"}).find_all("p")
    
    # For each paragraph...
    for paragraph in paragraphs:
        
        # Skip if there is no text (ie blank paragraph)
        if len(paragraph.text) == 0:
            continue
        
        # If the paragraph begins with a number (ie begins with a player ranking, indicating that it contains a header with player info)
        if paragraph.text[0] in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            
            # Extract the text
            line = paragraph.text
            
            # Fix bug for Ryan St. Louis, since we will be parsing the string by "."
            line = line.replace("St. Louis", "St Louis")
            
            # Retrieve the player rank and trim from the string
            rank = line.split(".")[0]
            line = line.split(".")[1].strip()
            
            # Retrieve the player name and position
            player = line.split(",")[0].strip()
            position = line.split(",")[1].strip()
            
            
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
            
            draft_df = pd.concat([draft_df, player_df])




#%% THE ATHLETIC (WHEELER)

# List the site name
site = "The Athletic"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2023 Draft
        #"https://theathletic.com/3470428/2022/08/08/top-nhl-prospects-draft/",
        ## 2022 Draft
        #"https://theathletic.com/3306659/2022/06/06/nhl-draft-top-100-prospects-ranking/",
        #"https://theathletic.com/2887391/2021/11/03/nhl-draft-ranking-scott-wheelers-top-64-prospects-for-2022/",
        #"https://theathletic.com/2811931/2021/09/15/the-2022-nhl-draft-wheeler-ranks-his-top-32-prospects-in-preseason/",
        ## 2021 Draft
        #"https://theathletic.com/2569641/2021/06/22/wheeler-nhl-drafts-top-100-prospects-for-2021-sees-michigan-players-top-the-ranking/",
        #"https://theathletic.com/2392340/2021/03/03/nhl-draft-2021-midseason-ranking-power/",
        #"https://theathletic.com/2200822/2020/12/01/nhl-draft-rankings-2021/",
        #"https://theathletic.com/2044746/2020/09/14/wheeler-preseason-ranking-for-the-2021-nhl-drafts-top-32-prospects/",
        ## 2020 Draft
        #"https://theathletic.com/2019544/2020/09/21/wheeler-updated-ranking-for-the-2020-nhl-drafts-top-100-prospects/",
        #"https://theathletic.com/1736440/2020/06/01/wheeler-final-ranking-for-the-2020-nhl-drafts-top-100-prospects/",
        #"https://theathletic.com/1598118/2020/02/19/wheeler-midseason-ranking-for-the-2020-nhl-drafts-top-62-prospects/",
        #"https://theathletic.com/1287064/2019/11/04/wheeler-preliminary-ranking-for-the-2020-nhl-drafts-top-62-prospects/",
        #"https://theathletic.com/1126042/2019/08/19/wheeler-preseason-look-at-the-top-31-prospects-for-the-2020-nhl-draft/",
        ## 2019 Draft
        #"https://theathletic.com/947751/2019/05/06/wheeler-final-ranking-for-the-2019-nhl-drafts-top-100-prospects/",
        #"https://theathletic.com/786254/2019/02/18/wheeler-midseason-ranking-for-the-2019-nhl-drafts-top-62-prospects/",
        #"https://theathletic.com/632965/2018/11/06/wheeler-preliminary-ranking-for-the-2019-nhl-drafts-top-62-prospects/",
        ## 2018 Draft
        "https://theathletic.com/342459/2018/05/08/wheeler-final-ranking-for-the-2018-nhl-drafts-top-100-prospects/",
        "https://theathletic.com/242723/2018/02/19/wheeler-midseason-ranking-for-the-2018-nhl-drafts-top-62-prospects/"
    ],
    "date":[
        ## 2023 Draft
        #"2022-08-08",
        ## 2022 Draft
        #"2022-06-06",
        #"2021-11-03",
        #"2021-09-15",
        ## 2021 Draft
        #"2021-06-22",
        #"2021-03-03",
        #"2020-12-01",
        #"2020-09-14",
        ## 2020 Draft
        #"2020-09-21",
        #"2020-06-01",
        #"2020-02-19",
        #"2019-11-04",
        #"2019-08-19",
        ## 2019 Draft
        #"2019-05-06",
        #"2019-02-18",
        #"2018-11-06",
        ## 2018 Draft
        "2018-05-08",
        "2018-02-19"
    ],
    "author":[
        ## 2023 Draft
        #"Scott Wheeler",
        ## 2022 Draft
        #"Scott Wheeler",
        #"Scott Wheeler",
        #"Scott Wheeler",
        ## 2021 Draft
        #"Scott Wheeler",
        #"Scott Wheeler",
        #"Scott Wheeler",
        #"Scott Wheeler",
        ## 2020 Draft
        #"Scott Wheeler",
        #"Scott Wheeler",
        #"Scott Wheeler",
        #"Scott Wheeler",
        #"Scott Wheeler",
        ## 2019 Draft
        #"Scott Wheeler",
        #"Scott Wheeler",
        #"Scott Wheeler",
        ## 2018 Draft
        "Scott Wheeler",
        "Scott Wheeler"
    ],
    "year":[
        ## 2023 Draft
        #2023,
        ## 2022 Draft
        #2022,
        #2022,
        #2022,
        ## 2021 Draft
        #2021,
        #2021,
        #2021,
        #2021,
        ## 2020 Draft
        #2020,
        #2020,
        #2020,
        #2020,
        #2020,
        ## 2019 Draft
        #2019,
        #2019,
        #2019,
        ## 2018 Draft
        2018,
        2018
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
    
    # Open link and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    
    # Retrieve results
    article_headers = soup.find("div", {"id":"article-container-grid"}).find_all("h3")
    
    # For each player header in the article
    for header in article_headers:
        
        if len(header.text) == 0:
            continue
        
        if header.text[0] in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            
            # Extract player information
            line = header.text
            
            line = line.replace("St. Louis", "St Louis")
            line = line.replace("36 Brett Leason", "36. Brett Leason")
            
            rank = line.split(".")[0]
            line = line.split(".")[1].strip()
            
            if "—" in line:
                player = line.split("—")[0].strip()
                line = line.split("—")[1].strip()
            elif "–" in line:
                player = line.split("–")[0].strip()
                line = line.split("–")[1].strip()
            elif ":" in line:
                player = line.split(":")[0].strip()
                line = line.split(":")[1].strip()
            else:
                print("ERROR")
            
            position = line.split(",")[0].strip()
            
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
            
            draft_df = pd.concat([draft_df, player_df])



#%% THE ATHLETIC (TABLE)

# List the site name
site = "The Athletic"


# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2022 Draft
        "https://theathletic.com/3321363/2022/05/31/nhl-draft-prospects/",
        ## 2021 Draft
        #"https://theathletic.com/2620093/2021/06/15/nhl-draft-prospects-ranking-2021-corey-pronmans-final-top-151/",
        ## 2020 Draft
        "https://theathletic.com/1769140/2020/06/16/pronmans-2020-nhl-draft-board-top-122-prospects/",
    ],
    "date":[
        ## 2022 Draft
        "2022-05-31",
        ## 2021 Draft
        #"2021-06-15",
        ## 2020 Draft
        "2020-06-16",
    ],
    "author":[
        ## 2022 Draft
        "Corey Pronman",
        ## 2021 Draft
        #"Corey Pronman"
        ## 2020 Draft
        "Corey Pronman",
    ],
    "year":[
        ## 2022 Draft
        2022,
        ## 2021 Draft
        #2021,
        ## 2020 Draft
        2020,
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
    
    # Open link and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # Retrieve results
    results_table = soup.find("tbody").find_all("tr")
    
    # For each player ranked...
    for row in results_table:
        
        # Extract player information
        rank = row.find_all("td")[0].text.strip()
        player = row.find_all("td")[1].text.strip()
        position = row.find_all("td")[2].text.strip()
        
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
        
        draft_df = pd.concat([draft_df, player_df])



#%% DOBBER PROSPECTS

# List the site name
site = "Dobber Prospects"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2021 Draft
        #"https://dobberprospects.com/2020/11/04/dp-scouting-teams-2021-nhl-draft-rankings-nov-2020/",
        #"https://dobberprospects.com/2020/08/12/dobberprospects-preliminary-2021-nhl-draft-rankings/",
        ## 2020 Draft
        #"https://dobberprospects.com/2020/10/02/robinson-the-actual-final-2020-nhl-draft-rankings-october-2020/",
        #"https://dobberprospects.com/2020/06/25/robinson-final-2020-nhl-draft-rankings-june-2020/",
        #"https://dobberprospects.com/2020/04/01/robinson-2020-nhl-draft-rankings-april-2020/",
        #"https://dobberprospects.com/2019/09/02/robinson-preliminary-2020-nhl-draft-rankings-sept-2019/",
        ## 2019 Draft
        #"https://dobberprospects.com/2019/06/19/robinson-final-2019-nhl-draft-rankings-june-2019/",
        #"https://dobberprospects.com/2019/05/15/cam-robinsons-2019-nhl-draft-rankings-april-2019/",
        #"https://dobberprospects.com/2019/02/06/cam-robinsons-2019-nhl-draft-rankings-top-100-february-2019/",
        #"https://dobberprospects.com/2018/12/20/2019-nhl-draft-rankings-wjc-mini-version-december-2018/",
        #"https://dobberprospects.com/2018/11/05/2019-nhl-draft-rankings-november-2018-edition/",
        ## 2018 Draft
        "https://dobberprospects.com/2018/06/15/cam-robinsons-2018-draft-rankings-top-130-final-edition/",
        "https://dobberprospects.com/2018/04/26/cam-robinsons-2018-nhl-draft-rankings-top-115-april-2018/",
        "https://dobberprospects.com/2018/03/20/cam-robinsons-2018-nhl-draft-rankings-top-100-march-2018/",
        "https://dobberprospects.com/2018/01/11/2018-nhl-draft-rankings-top-75-january-2018-edition/",
        "https://dobberprospects.com/2017/10/27/prospect-ramblings-2018-draft-rankings/",
        "https://dobberprospects.com/2017/08/14/cam-robinsons-2018-nhl-draft-rankings-august-2017-edition/"
    ],
    "date":[
        ## 2021 Draft
        #"2020-11-04",
        #"2020-08-12",
        ## 2020 Draft
        #"2020-10-02",
        #"2020-06-25",
        #"2020-04-01",
        #"2019-09-02",
        ## 2019 Draft
        #"2019-06-19",
        #"2019-05-15",
        #"2019-02-06",
        #"2018-12-20",
        #"2018-11-05",
        ## 2018 Draft
        "2018-06-15",
        "2018-04-26",
        "2018-03-20",
        "2018-01-11",
        "2017-10-27",
        "2017-08-14"
    ],
    "author":[
        ## 2021 Draft
        #"Full Staff",
        #"Full Staff",
        ## 2020 Draft
        #"Cam Robinson",
        #"Cam Robinson",
        #"Cam Robinson",
        #"Cam Robinson",
        ## 2019 Draft
        #"Cam Robinson",
        #"Cam Robinson",
        #"Cam Robinson",
        #"Cam Robinson",
        #"Cam Robinson",
        ## 2018 Draft
        "Cam Robinson",
        "Cam Robinson",
        "Cam Robinson",
        "Cam Robinson",
        "Cam Robinson",
        "Cam Robinson"
    ],
    "year":[
        ## 2021 Draft
        #2021,
        #2021,
        ## 2020 Draft
        #2020,
        #2020,
        #2020,
        #2020,
        ## 2019 Draft
        #2019,
        #2019,
        #2019,
        #2019,
        #2019,
        ## 2018 Draft
        2018,
        2018,
        2018,
        2018,
        2018,
        2018
    ],
    "organizer_type":[
        ## 2021 Draft
        #"team",
        #"team",
        ## 2020 Draft
        #"individual",
        #"individual",
        #"individual",
        #"individual",
        ## 2019 Draft
        #"individual",
        #"individual",
        #"individual",
        #"individual",
        #"individual",
        ## 2018 Draft
        "individual",
        "individual",
        "individual",
        "individual",
        "individual",
        "individual"
    ],
    "set_type":"rank"
})



# For each ranking set...
for i, row in resource_df.iterrows():
    
    rank = 1
    
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
    
    
    # Retrieve results
    article_headers = soup.find("div", {"class":"fusion-content-tb fusion-content-tb-1"}).find_all("ol")
    
    # For each player header in the article
    for header in article_headers:
        
        try:
            rank = int(header["start"])
        except:
            pass
        
        subheaders = header.find_all("li")
        
        for subheader in subheaders:
            
            if year == 2018:
                
                subheader_text = subheader.text.split("/")
                
                player = subheader_text[0].strip()
                position = subheader_text[1].strip()
                
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
                
                draft_df = pd.concat([draft_df, player_df])
                
                rank += 1
                
            else:
            
                try:
                        
                    subheader_text = subheader.text
                    
                    if "|" in subheader_text:
                        subheader_text = subheader_text.split("|")[0].strip()
                    else:
                        subheader_text = subheader_text.split("/")[0].strip()
                    
                    if subheader_text == "Drew Helleson. RHD":
                        subheader_text = subheader_text.replace(".", ",")
                    
                    player = subheader_text.split(",")[0].strip()
                    position = subheader_text.split(",")[1].strip()
                    
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
                    
                    draft_df = pd.concat([draft_df, player_df])
                except:
                    pass
                
                rank += 1



#%% DOBBER PROSPECTS (TABLE)

# List the site name
site = "Dobber Prospects"


# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2020 Draft
        "https://dobberprospects.com/2020/09/30/dobberprospects-final-2020-nhl-draft-rankings/",
    ],
    "date":[
        ## 2020 Draft
        "2020-09-30",
    ],
    "author":[
        ## 2020 Draft
        "Full Staff",
    ],
    "year":[
        ## 2020 Draft
        2020,
    ],
    "set_type":"rank",
    "organizer_type":"team"
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
    
    # Open link and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # Retrieve results
    results_table = soup.find("table", {"dir":"ltr"}).find("tbody").find_all("tr")[1:]
    
    # For each player ranked...
    for row in results_table:
        
        # Extract player information
        rank = row.find_all("td")[0].text.strip()
        player = row.find_all("td")[1].text.strip()
        position = row.find_all("td")[2].text.strip()
        
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
        
        draft_df = pd.concat([draft_df, player_df])





#%% THE DRAFT ANALYST

# List the site name
site = "The Draft Analyst"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2021 Draft
        ##"https://www.thedraftanalyst.com/2021-nhl-draft/2021-nhl-draft-january-draft-rankings/",
        ##"https://www.thedraftanalyst.com/2021-nhl-draft/2021-draft-final-ranking-1-224/",
        ## 2020 Draft
        "https://www.thedraftanalyst.com/2020-nhl-draft/final-draft-rankings-the-top-300/",
        "https://www.thedraftanalyst.com/rankings/updated-2020-nhl-draft-rankings-top-125-for-march/",
        "https://www.thedraftanalyst.com/2020-nhl-draft/2020-nhl-draft-midseason-top-300/",
        "https://www.thedraftanalyst.com/rankings/2020-draft-preliminary-rankings-and-watch-list-2/"
    ],
    "date":[
        ## 2021 Draft
        ##"2021-01-21",
        ##"2021-07-03",
        ## 2020 Draft
        "2020-06-05",
        "2020-03-02",
        "2020-01-13",
        "2019-08-24"
    ],
    "author":[
        ## 2021 Draft
        ##"Steve Kournianos",
        ##"Steve Kournianos",
        ## 2020 Draft
        "Steve Kournianos",
        "Steve Kournianos",
        "Steve Kournianos",
        "Steve Kournianos"
    ],
    "year":[
        # # 2021 Draft
        ## 2021,
        ## 2021,
        # # 2020 Draft
        2020,
        2020,
        2020,
        2020
    ],
    "set_type":"rank",
    "organizer_type":"team"
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
    
    # Open link and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # Extract table rows
    table_rows = soup.find("table", {"id":"myTable"}).find("tbody").find_all("tr")
    
    # For each row...
    for row in table_rows:
        
        # Retrieve player information
        rank = row.find_all("td")[0].text.strip()
        if date in ["2020-03-02"]:
            player = row.find_all("td")[2].text.strip()
            position = row.find_all("td")[3].text.strip()
        else:
            player = row.find_all("td")[1].text.strip()
            position = row.find_all("td")[2].text.strip()
        
        if date in ["2020-03-02", "2020-06-05"]:
            first = player.split(",")[1].strip()
            last = player.split(",")[0].strip()
            player = first + " " + last
        
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
        
        draft_df = pd.concat([draft_df, player_df])






#%% SMAHT SCOUTING

# List the site name
site = "Smaht Scouting"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2022 Draft
        #"https://smahtscouting.com/2022/05/24/final-2022-nhl-draft-rankings/",
        #"https://smahtscouting.com/2022/01/23/winter-2022-nhl-draft-rankings/",
        #"https://smahtscouting.com/2021/10/26/preliminary-2022-nhl-draft-rankings/",
        ## 2021 Draft
        #"https://smahtscouting.com/2021/06/12/final-2021-nhl-draft-rankings/",
        #"https://smahtscouting.com/2021/02/11/winter-2021-nhl-draft-rankings/",
        #"https://smahtscouting.com/2020/11/28/2021-nhl-draft-preliminary-rankings/",
        ## 2020 Draft
        "https://smahtscouting.com/2020/08/16/final-2020-nhl-draft-rankings/"
    ],
    "date":[
        ## 2022 Draft
        #"2022-05-24",
        #"2022-01-23",
        #"2021-10-26",
        ## 2021 Draft
        #"2021-06-12",
        #"2021-02-11",
        #"2020-11-28",
        ## 2020 Draft
        "2020-08-16"
    ],
    "author":[
        ## 2022 Draft
        #"Full Staff",
        #"Full Staff",
        #"Full Staff",
        ## 2021 Draft
        #"Full Staff",
        #"Full Staff",
        #"Full Staff",
        ## 2020 Draft
        "Full Staff"
    ],
    "year":[
        # # 2022 Draft
        # 2022,
        # 2022,
        # 2022,
        # # 2021 Draft
        # 2021,
        # 2021,
        # 2021,
        # # 2020 Draft
        2020
    ],
    "set_type":"rank",
    "organizer_type":"team"
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
    
    # Open link and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # Extract table rows
    table_rows = soup.find("figure", {"class":"wp-block-table"}).find("table").find("tbody").find_all("tr")[1:]
    
    # For each row...
    for row in table_rows:
        
        # Retrieve player information
        rank = row.find_all("td")[0].text.strip()
        player = row.find_all("td")[1].text.strip()
        if year > 2020:
            position = row.find_all("td")[3].text.strip()
        else:
            position = row.find_all("td")[4].text.strip()
        
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
        
        draft_df = pd.concat([draft_df, player_df])






#%% MCKEEN'S HOCKEY

# List the site name
site = "McKeen's Hockey"





#%% FUTURE CONSIDERATIONS

# Note: The future considerations hockey draft board updates whenever they put out a new list for each draft year;
#       because of this, we have to be careful to only 

# List the site name
site = "FC Hockey"
author = "Full Staff"
date = "2022-06-28"
year = 2022
set_type = "rank"
organizer_type = "team"
url = "https://nhlentrydraft.com/rankings/page/"
pages = [1,2,3]


for page in pages:
    
    # Open link and extract page data
    driver.get(url + str(page) + "/")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # Retrieve ranking information
    table_rows = soup.find("div", {"class":"container"}).find("table").find("tbody").find_all("tr")
    
    for row in table_rows:
        
        rank = row.find_all("td")[0].text.strip()
        last = row.find_all("td")[2].find("a").find("i").text.strip()
        first = row.find_all("td")[2].find("a").text.replace(last, "").strip()
        player = first + " " + last
        position = row.find_all("td")[3].text.strip()
        
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
        
        draft_df = pd.concat([draft_df, player_df])







#%% THE HOCKEY NEWS

# List the site name
site = "The Hockey News"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2020 Draft
        #"https://thehockeynews.com/news/final-2020-nhl-draft-rankings-these-go-to-120",
        ## 2019 Draft
        #"https://thehockeynews.com/all-access/the-hockey-news-top-100-prospects-for-the-2019-nhl-draft",
        ## 2017 Draft
        "https://thehockeynews.com/news/2017-nhl-draft-ranking-the-top-120-prospects"
    ],
    "date":[
        ## 2020 Draft
        #"2020-05-11",
        ## 2019 Draft
        #"2019-04-26",
        ## 2017 Draft
        "2017-06-16"
    ],
    "author":[
        ## 2020 Draft
        #"Ryan Kennedy",
        ## 2019 Draft
        #"Ryan Kennedy",
        ## 2017 Draft
        "Ryan Kennedy"
    ],
    "year":[
        ## 2020 Draft
        #2020,
        ## 2019 Draft
        #2019,
        ## 2017 Draft
        2017
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
    
    # Open link and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    
    # Retrieve results
    paragraphs = soup.find("div", {"class":"m-detail--body"}).find("ol").find_all("li")
    
    # Initialize rank
    rank = 0
    
    # For each player header in the article
    for paragraph in paragraphs:
        
        if len(paragraph.text) == 0:
            continue
        
        rank += 1
    
        
        # Extract player information
        line = paragraph.text
        
        player = line.split(",")[0].strip()
        position = line.split(",")[1].strip()
        
        # Store data in draft_df
        player_df = pd.DataFrame({
            "resource_site":[site], 
            "resource_staff":[author], 
            "resource_date":[date],
            "resource_url":[url], 
            "rank":[str(rank)], 
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
        
        draft_df = pd.concat([draft_df, player_df])





#%% ELITE PROSPECTS

# List the site name
site = "Elite Prospects"




#%% DAILY FACEOFF

# List the site name
site = "Daily Faceoff"




#%% HOCKEYPROSPECT.COM

# List the site name
site = "hockeyprospect.com"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2023 Draft
        "https://hockeyprospect.com/very-early-2023-nhl-draft-ranking-june-2022/"
    ],
    "date":[
        ## 2023 Draft
        "2022-07-27"
    ],
    "author":[
        ## 2023 Draft
        "Full Staff"
    ],
    "year":[
        ## 2023 Draft
        2023
    ],
    "set_type":"rank",
    "organizer_type":"team"
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
    
    # Open link and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # Extract table rows
    table_rows = soup.find("table", {"id":"tablepress-365"}).find("tbody").find_all("tr")
    
    # For each row...
    for row in table_rows:
        
        # Retrieve player information
        rank = row.find_all("td")[0].text.strip()
        last_name = row.find_all("td")[1].text.strip()
        first_name = row.find_all("td")[2].text.strip()
        player = first_name + " " + last_name
        position = row.find_all("td")[5].text.strip()
        
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
        
        draft_df = pd.concat([draft_df, player_df])





#%% NHL.COM

# List the site name
site = "NHL.com"


# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2020 Draft
        #"https://www.nhl.com/news/2020-nhl-draft-top-prospects/c-316240380",
        #"https://www.nhl.com/news/top-prospects-eligible-for-2020-nhl-draft/c-315889038",
        #"https://www.nhl.com/news/top-prospects-eligible-2020-nhl-draft-lafreniere-perfetti/c-312159422",
        "https://www.nhl.com/news/top-prospects-eligible-for-2020-nhl-draft/c-309776500"
    ],
    "date":[
        ## 2020 Draft
        #"2020-03-30",
        #"2020-03-05",
        #"2019-12-04",
        "2019-10-06"
    ],
    "author":[
        ## 2020 Draft
        #"Mike G. Morreale",
        #"Mike G. Morreale",
        #"Mike G. Morreale",
        "Mike G. Morreale"
    ],
    "year":[
        ## 2020 Draft
        #2020,
        #2020,
        #2020,
        2020
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
    
    # Open link and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # Retrieve results
    article_body = soup.find("div", {"class":"article-item__body"}).find_all("b")
    
    # For each player ranked...
    for bold_text in article_body:
        
        # Extract player information
        line = bold_text.text
        
        if line[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            
            line = re.sub("[\(\[].*?[\)\]]", "", line)
            
            line = line.replace("St. Louis", "St Louis")
            
            rank = line.split(".")[0]
            line = line.split(".")[1].strip()
            
            player = line.split(",")[0].strip()
            position = line.split(",")[1].strip()
            
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
            
            draft_df = pd.concat([draft_df, player_df])



#%% PUCK AUTHORITY

# List the site name
site = "Puck Authority"



#%% ESPN

# List the site name
site = "ESPN"


# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2020 Draft
        #"https://www.espn.com/nhl/insider/story/_/id/29994322/2020-nhl-draft-rankings-final-top-100-prospects-class-chris-peters-plus-position-rankings",
        #"https://www.espn.com/nhl/insider/story/_/id/29383468/2020-nhl-draft-rankings-top-100-prospects-class-chris-peters",
        #"https://www.espn.com/nhl/insider/story/_/id/28576622/2020-nhl-draft-rankings-chris-peters-top-50-prospects",
        "https://www.espn.com/nhl/insider/story/_/id/27896100/2020-nhl-draft-rankings-peters-updated-early-season-top-25-prospects"
    ],
    "date":[
        ## 2020 Draft
        #"2020-10-01",
        #"2020-06-30",
        #"2020-01-29",
        "2019-10-22"
    ],
    "author":[
        ## 2020 Draft
        #"Chris Peters",
        #"Chris Peters",
        #"Chris Peters",
        "Chris Peters"
    ],
    "year":[
        ## 2020 Draft
        #2020,
        #2020,
        #2020,
        2020
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
    
    # Open link and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # Retrieve results
    article_body = soup.find("div", {"class":"article-body"}).find_all("h2")
    
    # For each player ranked...
    for header in article_body:
        
        # Extract player information
        line = header.text
        
        if line[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            
            
            line = line.replace("St. Louis", "St Louis")
            
            rank = line.split(".")[0]
            line = line.split(".")[1].strip()
            
            player = line.split(",")[0].strip()
            position = line.split(",")[1].strip()
            
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
            
            draft_df = pd.concat([draft_df, player_df])


#%% RAW CHARGE

# List the site name
site = "Raw Charge"

# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        ## 2020 Draft
        "https://www.rawcharge.com/2020/9/22/21446724/2020-nhl-draft-the-final-top-31-rankings-alexis-lafreniere-is-good-prospects-new-york-rangers",
        "https://www.rawcharge.com/2020/1/22/21075402/2020-nhl-draft-midseason-top-31-ranking-alexis-lafreniere-quinton-byfield-lucas-raymond-prospects",
        "https://www.rawcharge.com/2019/9/12/20861418/2020-nhl-draft-rankings-the-preseason-top-31-prospects-entry-notes-lafrenierre-raymond-holtz-byfield"
    ],
    "date":[
        ## 2020 Draft
        "2020-09-22",
        "2020-01-22",
        "2019-09-12"
    ],
    "author":[
        ## 2020 Draft
        "Lauren Kelly",
        "Lauren Kelly",
        "Lauren Kelly"
    ],
    "year":[
        ## 2020 Draft
        2020,
        2020,
        2020
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
    
    # Open link and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # Extract table rows
    table_rows = soup.find("table", {"class":"p-data-table dataTable"}).find("tbody").find_all("tr")
    
    # For each row...
    for row in table_rows:
        
        row_len = len(row.find_all("td"))
        
        # Retrieve player information
        rank = row.find_all("td")[0].text.strip()
        player = row.find_all("td")[row_len - 6].text.strip()
        position = row.find_all("td")[row_len - 4].text.strip()
        
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
        
        draft_df = pd.concat([draft_df, player_df])


#%% EYES ON THE PRIZE (CONSOLIDATED)

# List the site name
site = "SB Nation"


# Create a data frame with resource URL's and various information about the ranking sets
resource_df = pd.DataFrame({
    "url":[
        "https://www.habseyesontheprize.com/2022/7/3/23192056/2022-nhl-draft-rankings-consensus-wright-slafkovsky-cooley-bob-mckenzie-athletic-prospects-elite",
        #"https://www.habseyesontheprize.com/2021/7/22/22588437/2021-nhl-draft-rankings-consensus-power-beniers-lysell-bob-mckenzie-athletic-hockey-prospects-elite",
        #"https://www.habseyesontheprize.com/nhl-entry-draft-picks-2020/2020/10/5/21502714/2020-nhl-draft-rankings-consensus-lafreniere-byfield-stutzle-bob-mckenzie-athletic-hockey-prospects",
        #"https://www.habseyesontheprize.com/nhl-entry-draft-picks-2019/2019/6/21/18692160/2019-nhl-draft-rankings-consensus-hughes-kakko-bob-mckenzie-athletic-hockey-prospects",
        #"https://www.habseyesontheprize.com/nhl-entry-draft-picks-2018/2018/6/20/17481500/2018-nhl-draft-rankings-consensus-jesperi-kotkaniemi-bob-mckenzie-athletic-hockey-prospects",
        #"https://www.habseyesontheprize.com/nhl-entry-draft-picks-2017/2017/6/21/15832840/2017-nhl-draft-rankings-tsn-sportsnet-espn-hockey-prospect-iss-bob-mckenzie-craig-button"
    ],
    "date":[
        "2022-07-03",
        #"2021-07-22",
        #"2020-10-05",
        #"2019-06-21",
        #"2018-06-20",
        #"2017-06-21"
    ],
    "year":[
        2022,
        #2021,
        #2020,
        #2019,
        #2018,
        #2017
    ]
})


# For each ranking set...
for i, row in resource_df.iterrows():
    
    # Retrieve information about the ranking set
    url = row["url"]
    date = row["date"]
    year = row["year"]
    
    
    # Open link to rankings and extract page data
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    
    # Retrieve rankings table
    data_table = soup.find("div", {"id":"b27K1A"}).find("tbody").find_all("tr")
    
    
    # For each row in the rankings table (ie each player)...
    for row in data_table:
        
        # Extract player data
        rank = row.find_all("td")[0].text.strip()
        player = row.find_all("td")[1].text.strip().title()
        #first = row.find_all("td")[1].text.strip().split(", ")[1].title()
        #last = row.find_all("td")[1].text.strip().split(", ")[0].title()
        #player = first + " " + last
        position = row.find_all("td")[5].text.strip()
        
        
        # If the row has no player, then skip...
        if player == "":
            continue
        
    
        # Store data in draft_df
        player_df = pd.DataFrame({
            "resource_site":[site], 
            "resource_staff":[np.nan], 
            "resource_date":[date],
            "resource_url":[url], 
            "rank":[rank], 
            "player":[player],
            "position":[position],
            "team":[np.nan],
            "year":[year],
            "set_type":["consolidated"],
            "organizer_type":["individual"],
            "retrieval_method":["scrape"],
            "league_subset":[np.nan],
            "region_subset":[np.nan],
            "position_subset":[np.nan]
        })
        
        draft_df = pd.concat([draft_df, player_df])




#%% DATA CLEANING

# Create backup version of the draft data
backup = draft_df.copy()

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




#%% SAVE NEW DATA

# Load previous data
draft_df_orig = pd.read_csv("Data/rankings/ranking_data.csv")

# Save the original data as backup
draft_df_orig.to_csv("Data/rankings/ranking_data_backup.csv", index = False)

# Add in the newly scraped data
draft_df_new = pd.concat([draft_df_orig, draft_df]).reset_index(drop = True)

# Save the new data
draft_df_new.to_csv("Data/rankings/ranking_data.csv", index = False)





