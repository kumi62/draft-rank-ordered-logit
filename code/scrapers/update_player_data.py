#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 22:20:01 2022

@author: brendankumagai

The purpose of this file is to update the "player_data.csv" and scrape player
statistics and information from Elite Prospects.

In this file, we will:
    
    i) Fill in the blanks for any new players in "player_data.csv" by extracting
       first and last name, scraping the player's Elite Prospects url, and creating
       unique player IDs based on the EP ID and draft year.
    
    ii) Scrape new player statistics and information from Elite Prospects.
"""


#%% LOAD DATA AND PACKAGES

# Load packages
import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
from unidecode import unidecode
import re 

# Set directory
os.chdir("/Users/brendankumagai/Sports-Analytics/2022-02_Plackett_Luce_Draft_Model")

# Remove SettingWithCopyWarning when calling df.loc[index, colname]
pd.options.mode.chained_assignment = None

# Start webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Load previous data
player_data = pd.read_csv("Data/players/player_data.csv")



#%% SCRAPE NEW PLAYER URLS

# Note: This may take a few tries as Google prevents repetitive scraping.
# Rerun this cell along with cells above and below on repeat until all urls
# are scraped.


# Create list to store player urls
player_urls = []

# For each player in player_data
for i, row in player_data.iterrows():
    
    try:
        # Print player name
        print(row["player"])
        
        # Extract current url value
        row_url = str(row["url"])
        
        # If the row has no URL...
        if row_url == "nan":
            
            # Google the player
            driver.get("https://www.google.com/search?q=" + row["player"] + "+elite+prospects")
            time.sleep(5)
            
            # Extract page source code
            soup = BeautifulSoup(driver.page_source, "lxml")
            
            # Find the first link
            link = soup.find("div", {"class":"v7W49e"}).find_all("div")[0].find("a")["href"]
            
            # Add to player_urls
            player_urls.append(link)
            
        # If the row has an URL...
        else:
            # Add url to player_urls
            player_urls.append(row_url)
        
    except:
        
        print("--Issue in scraping! Skipped player!")
        player_urls.append(np.nan)




#%% TEMP: SAVE UPDATED URLS

# Update url column
player_data["url"] = player_urls

# Save updated urls
player_data.to_csv("Data/players/player_data.csv", index = False)




#%% FILL IN MISSING PLAYER INFORMATION

# Check for duplicated players
url_counts = player_data.groupby(["draft_year", "url"]).size()
url_counts2 = player_data.groupby(["url"]).size()

# Obtain first and last names (Note: This may need a manual sanity check afterwards)
player_data["first_name"] = np.where(player_data["first_name"].isnull(), player_data["player"].str.split(" ").str[0].str.strip(), player_data["first_name"])
player_data["last_name"] = np.where(player_data["last_name"].isnull(), player_data["player"].str.split(" ").str[1].str.strip(), player_data["last_name"])

# Obtain EP ID and create player ID
player_data["ep_id"] = np.where(player_data["ep_id"].isnull(), player_data["url"].str.split("/").str[4], player_data["ep_id"])
player_data["player_id"] = np.where(player_data["player_id"].isnull(), player_data["draft_year"].astype(str) + "_" + player_data["ep_id"].astype(str), player_data["player_id"])

# Save updated data
player_data.to_csv("Data/players/player_data.csv", index = False)



#%% SCRAPE PLAYER INFORMATION AND STATISTICS

# Load in previous data
info_df = pd.read_csv("Data/players/player_information.csv")
sk_stats_df = pd.read_csv("Data/players/skater_statistics.csv")
gl_stats_df = pd.read_csv("Data/players/goalie_statistics.csv")

# Obtain list of urls already scraped
urls_scraped = info_df["source"].tolist()

# Obtain list of unique urls in player data
urls_unique = list(set(player_data["url"].tolist()))

# Remove urls that have already been scraped
urls = list(set(urls_unique) - set(urls_scraped))

# Initialize list to store urls that were not scraped
missed_urls = []

# Get today's date
today = datetime.today().strftime('%Y-%m-%d')

i = 0

# For each player url...
for url in urls:
    
    i+= 1
    print(i)
    
    try:
        # Extract Elite Prospects ID
        ep_id = url.split("/")[4]
        print(ep_id)
        
        # Open link to rankings and extract page data
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "lxml")
        
        # Extract player information
        info_blocks = soup.find("div", {"class":"ep-list"}).find_all("div", recursive = False)
        
        date1 = info_blocks[0].find_all("div", recursive = False)[1].text.strip()
        date2 = info_blocks[0].find_all("div", recursive = False)[1].find("a")["href"].split("=")[1].split("&")[0].strip()
        
        pos = info_blocks[1].find_all("div", recursive = False)[1].text.strip()
        height = info_blocks[3].find_all("div", recursive = False)[1].text.strip()
        birthplace = info_blocks[4].find_all("div", recursive = False)[1].text.strip()
        weight = info_blocks[5].find_all("div", recursive = False)[1].text.strip()
        nation = info_blocks[6].find_all("div", recursive = False)[1].text.strip()
        handedness = info_blocks[7].find_all("div", recursive = False)[1].text.strip()
        
        row_df = pd.DataFrame({
            "ep_id":[ep_id], "birthdate":[date2], "birthdate_backup":[date1], "pos":[pos], "height":[height], "weight":[weight],
            "birthplace":[birthplace], "nation":[nation], "handedness":[handedness], "date_retrieved":[today], "source":[url]
        })
        
        # Add player information to info_df
        info_df = pd.concat([info_df, row_df])
        
        if pos == "G":
            
            try:
                
                league_table = soup.find("div", {"id":"league-stats"}).find("tbody").find_all("tr")
                
                for event in league_table:
                                        
                    try:
                        season = event.find("td", {"class":"season sorted"}).text.strip()
                    except:
                        season = np.nan
                    
                    try:
                        team = event.find("td", {"class":"team"}).text.strip()
                    except:
                        team = np.nan
                        
                    try:
                        league_nation_code = event.find("td", {"class":"league"}).find("img")["src"].split("/")[5].split(".")[0].strip()
                    except:
                        league_nation_code = np.nan
                        
                    try:
                        league = event.find("td", {"class":"league"}).text.strip()
                        league_url = event.find("td", {"class":"league"}).find("a")["href"].strip()
                    except:
                        league = np.nan
                        league_url = np.nan
                    
                    try:
                        reg_gp = event.find("td", {"class":"regular gp"}).text.strip()
                    except:
                        reg_gp = np.nan
                    
                    try:
                        reg_gd = event.find("td", {"class":"regular gd"}).text.strip()
                    except:
                        reg_gd = np.nan
                    
                    try:
                        reg_gaa = event.find("td", {"class":"regular gaa"}).text.strip()
                    except:
                        reg_gaa = np.nan
                    
                    try:
                        reg_svp = event.find("td", {"class":"regular svp"}).text.strip()
                    except:
                        reg_svp = np.nan
                    
                    try:
                        reg_ga = event.find("td", {"class":"regular ga"}).text.strip()
                    except:
                        reg_ga = np.nan
                    
                    try:
                        reg_svs = event.find("td", {"class":"regular svs"}).text.strip()
                    except:
                        reg_svs = np.nan
                    
                    try:
                        reg_so = event.find("td", {"class":"regular so"}).text.strip()
                    except:
                        reg_so = np.nan
                    
                    try:
                        reg_rec = event.find("td", {"class":"regular wlt"}).text.strip()
                    except:
                        reg_rec = np.nan
                    
                    try:
                        reg_toi = event.find("td", {"class":"regular toi"}).text.strip()
                    except:
                        reg_toi = np.nan
                    
                    try:
                        post_type = event.find("td", {"class":"postseason"}).text.strip()
                    except:
                        post_type = np.nan
                        
                    try:
                        post_gp = event.find("td", {"class":"postseason gp"}).text.strip()
                    except:
                        post_gp = np.nan
                    
                    try:
                        post_gd = event.find("td", {"class":"postseason gd"}).text.strip()
                    except:
                        post_gd = np.nan
                    
                    try:
                        post_gaa = event.find("td", {"class":"postseason gaa"}).text.strip()
                    except:
                        post_gaa = np.nan
                    
                    try:
                        post_svp = event.find("td", {"class":"postseason svp"}).text.strip()
                    except:
                        post_svp = np.nan
                    
                    try:
                        post_ga = event.find("td", {"class":"postseason ga"}).text.strip()
                    except:
                        post_ga = np.nan
                    
                    try:
                        post_svs = event.find("td", {"class":"postseason svs"}).text.strip()
                    except:
                        post_svs = np.nan
                    
                    try:
                        post_so = event.find("td", {"class":"postseason so"}).text.strip()
                    except:
                        post_so = np.nan
                    
                    try:
                        post_rec = event.find("td", {"class":"postseason wlt"}).text.strip()
                    except:
                        post_rec = np.nan
                    
                    try:
                        post_toi = event.find("td", {"class":"postseason toi"}).text.strip()
                    except:
                        post_toi = np.nan
                    
                    row_df = pd.DataFrame({
                        "ep_id":[ep_id], "event_type":["league"],
                        "season":[season], "team":[team], "league":[league], "league_url":[league_url], "league_nation_code":[league_nation_code],
                        "reg_gp":[reg_gp], "reg_gd":[reg_gd], "reg_gaa":[reg_gaa], "reg_svp":[reg_svp], "reg_ga":[reg_ga], "reg_svs":[reg_svs], "reg_so":[reg_so], "reg_rec":[reg_rec], "reg_toi":[reg_toi],
                        "post_type":[post_type], "post_gp":[post_gp], "post_gd":[post_gd], "post_gaa":[post_gaa], "post_svp":[post_svp], "post_ga":[post_ga], "post_svs":[post_svs], "post_so":[post_so], "post_rec":[post_rec], "post_toi":[post_toi],
                        "date_retrieved":[today], "source":[url]
                    })
                    
                    gl_stats_df = pd.concat([gl_stats_df, row_df])
                
                
            except:
                print("--Season stats unavailable or not scraped")
                pass
            
            
            try:
                
                tournament_table = soup.find("div", {"id":"cup-stats"}).find("tbody").find_all("tr")
                
                for event in tournament_table:
                    
                    try:
                        season = event.find("td", {"class":"season sorted"}).text.strip()
                    except:
                        season = np.nan
                    
                    try:
                        team = event.find("td", {"class":"team"}).text.strip()
                    except:
                        team = np.nan
                        
                    try:
                        league_nation_code = event.find("td", {"class":"league"}).find("img")["src"].split("/")[5].split(".")[0].strip()
                    except:
                        league_nation_code = np.nan
                        
                    try:
                        league = event.find("td", {"class":"league"}).text.strip()
                        league_url = event.find("td", {"class":"league"}).find("a")["href"].strip()
                    except:
                        league = np.nan
                        league_url = np.nan
                    
                    try:
                        reg_gp = event.find("td", {"class":"regular gp"}).text.strip()
                    except:
                        reg_gp = np.nan
                    
                    try:
                        reg_gd = event.find("td", {"class":"regular gd"}).text.strip()
                    except:
                        reg_gd = np.nan
                    
                    try:
                        reg_gaa = event.find("td", {"class":"regular gaa"}).text.strip()
                    except:
                        reg_gaa = np.nan
                    
                    try:
                        reg_svp = event.find("td", {"class":"regular svp"}).text.strip()
                    except:
                        reg_svp = np.nan
                    
                    try:
                        reg_ga = event.find("td", {"class":"regular ga"}).text.strip()
                    except:
                        reg_ga = np.nan
                    
                    try:
                        reg_svs = event.find("td", {"class":"regular svs"}).text.strip()
                    except:
                        reg_svs = np.nan
                    
                    try:
                        reg_so = event.find("td", {"class":"regular so"}).text.strip()
                    except:
                        reg_so = np.nan
                    
                    try:
                        reg_rec = event.find("td", {"class":"regular wlt"}).text.strip()
                    except:
                        reg_rec = np.nan
                    
                    try:
                        reg_toi = event.find("td", {"class":"regular toi"}).text.strip()
                    except:
                        reg_toi = np.nan
                    
                    try:
                        post_type = event.find("td", {"class":"postseason"}).text.strip()
                    except:
                        post_type = np.nan
                        
                    try:
                        post_gp = event.find("td", {"class":"postseason gp"}).text.strip()
                    except:
                        post_gp = np.nan
                    
                    try:
                        post_gd = event.find("td", {"class":"postseason gd"}).text.strip()
                    except:
                        post_gd = np.nan
                    
                    try:
                        post_gaa = event.find("td", {"class":"postseason gaa"}).text.strip()
                    except:
                        post_gaa = np.nan
                    
                    try:
                        post_svp = event.find("td", {"class":"postseason svp"}).text.strip()
                    except:
                        post_svp = np.nan
                    
                    try:
                        post_ga = event.find("td", {"class":"postseason ga"}).text.strip()
                    except:
                        post_ga = np.nan
                    
                    try:
                        post_svs = event.find("td", {"class":"postseason svs"}).text.strip()
                    except:
                        post_svs = np.nan
                    
                    try:
                        post_so = event.find("td", {"class":"postseason so"}).text.strip()
                    except:
                        post_so = np.nan
                    
                    try:
                        post_rec = event.find("td", {"class":"postseason wlt"}).text.strip()
                    except:
                        post_rec = np.nan
                    
                    try:
                        post_toi = event.find("td", {"class":"postseason toi"}).text.strip()
                    except:
                        post_toi = np.nan
                    
                    row_df = pd.DataFrame({
                        "ep_id":[ep_id], "event_type":["tournament"],
                        "season":[season], "team":[team], "league":[league], "league_url":[league_url], "league_nation_code":[league_nation_code],
                        "reg_gp":[reg_gp], "reg_gd":[reg_gd], "reg_gaa":[reg_gaa], "reg_svp":[reg_svp], "reg_ga":[reg_ga], "reg_svs":[reg_svs], "reg_so":[reg_so], "reg_rec":[reg_rec], "reg_toi":[reg_toi],
                        "post_type":[post_type], "post_gp":[post_gp], "post_gd":[post_gd], "post_gaa":[post_gaa], "post_svp":[post_svp], "post_ga":[post_ga], "post_svs":[post_svs], "post_so":[post_so], "post_rec":[post_rec], "post_toi":[post_toi],
                        "date_retrieved":[today], "source":[url]
                    })
                    
                    gl_stats_df = pd.concat([gl_stats_df, row_df])
                
                
            except:
                print("--Tournament stats unavailable or not scraped")
                pass
            
            
        else:
            
            
            # Extract player league statistics
            try:
                league_table = soup.find("div", {"id":"league-stats"}).find("tbody").find_all("tr")
                
                for event in league_table:
                    
                    try:
                        season = event.find("td", {"class":"season sorted"}).text.strip()
                    except:
                        season = np.nan
                    
                    try:
                        team = event.find("td", {"class":"team"}).text.strip()
                    except:
                        team = np.nan
                        
                    try:
                        league_nation_code = event.find("td", {"class":"league"}).find("img")["src"].split("/")[5].split(".")[0].strip()
                    except:
                        league_nation_code = np.nan
                        
                    try:
                        league = event.find("td", {"class":"league"}).text.strip()
                        league_url = event.find("td", {"class":"league"}).find("a")["href"].strip()
                    except:
                        league = np.nan
                        league_url = np.nan
                    
                    try:
                        reg_gp = event.find("td", {"class":"regular gp"}).text.strip()
                    except:
                        reg_gp = np.nan
                    
                    try:
                        reg_g = event.find("td", {"class":"regular g"}).text.strip()
                    except:
                        reg_g = np.nan
                    
                    try:
                        reg_a = event.find("td", {"class":"regular a"}).text.strip()
                    except:
                        reg_a = np.nan
                    
                    try:
                        reg_tp = event.find("td", {"class":"regular tp"}).text.strip()
                    except:
                        reg_tp = np.nan
                    
                    try:
                        reg_pim = event.find("td", {"class":"regular pim"}).text.strip()
                    except:
                        reg_pim = np.nan
                    
                    try:
                        reg_pm = event.find("td", {"class":"regular pm"}).text.strip()
                    except:
                        reg_pm = np.nan
                    
                    try:
                        post_type = event.find("td", {"class":"postseason"}).text.strip()
                    except:
                        post_type = np.nan
                    
                    try:
                        post_gp = event.find("td", {"class":"postseason gp"}).text.strip()
                    except:
                        post_gp = np.nan
                    
                    try:
                        post_g = event.find("td", {"class":"postseason g"}).text.strip()
                    except:
                        post_g = np.nan
                    
                    try:
                        post_a = event.find("td", {"class":"postseason a"}).text.strip()
                    except:
                        post_a = np.nan
                    
                    try:
                        post_tp = event.find("td", {"class":"postseason tp"}).text.strip()
                    except:
                        post_tp = np.nan
                    
                    try:
                        post_pim = event.find("td", {"class":"postseason pim"}).text.strip()
                    except:
                        post_pim = np.nan
                    
                    try:
                        post_pm = event.find("td", {"class":"postseason pm"}).text.strip()
                    except:
                        post_pm = np.nan
                    
                    
                    row_df = pd.DataFrame({
                        "ep_id":[ep_id], "event_type":["league"],
                        "season":[season], "team":[team], "league":[league], "league_url":[league_url], "league_nation_code":[league_nation_code],
                        "reg_gp":[reg_gp], "reg_g":[reg_g], "reg_a":[reg_a], "reg_pts":[reg_tp], "reg_pim":[reg_pim], "reg_pm":[reg_pm],
                        "post_type":[post_type], "post_gp":[post_gp], "post_g":[post_g], "post_a":[post_a], "post_pts":[post_tp], "post_pim":[post_pim], "post_pm":[post_pm],
                        "date_retrieved":[today], "source":[url]
                    })
                    
                    sk_stats_df = pd.concat([sk_stats_df, row_df])
            except:
                print("--Season stats unavailable or not scraped")
                pass
            
            
            # Extract player tournament statistics
            try:
                tournament_table = soup.find("div", {"id":"cup-stats"}).find("tbody").find_all("tr")
                
                for event in tournament_table:
                    
                    try:
                        season = event.find("td", {"class":"season sorted"}).text.strip()
                    except:
                        season = np.nan
                    
                    try:
                        team = event.find("td", {"class":"team"}).text.strip()
                    except:
                        team = np.nan
                        
                    try:
                        league_nation_code = event.find("td", {"class":"league"}).find("img")["src"].split("/")[5].split(".")[0].strip()
                    except:
                        league_nation_code = np.nan
                        
                    try:
                        league = event.find("td", {"class":"league"}).text.strip()
                        league_url = event.find("td", {"class":"league"}).find("a")["href"].strip()
                    except:
                        league = np.nan
                        league_url = np.nan
                    
                    try:
                        reg_gp = event.find("td", {"class":"regular gp"}).text.strip()
                    except:
                        reg_gp = np.nan
                    
                    try:
                        reg_g = event.find("td", {"class":"regular g"}).text.strip()
                    except:
                        reg_g = np.nan
                    
                    try:
                        reg_a = event.find("td", {"class":"regular a"}).text.strip()
                    except:
                        reg_a = np.nan
                    
                    try:
                        reg_tp = event.find("td", {"class":"regular tp"}).text.strip()
                    except:
                        reg_tp = np.nan
                    
                    try:
                        reg_pim = event.find("td", {"class":"regular pim"}).text.strip()
                    except:
                        reg_pim = np.nan
                    
                    try:
                        reg_pm = event.find("td", {"class":"regular pm"}).text.strip()
                    except:
                        reg_pm = np.nan
                    
                    try:
                        post_type = event.find("td", {"class":"postseason"}).text.strip()
                    except:
                        post_type = np.nan
                    
                    try:
                        post_gp = event.find("td", {"class":"postseason gp"}).text.strip()
                    except:
                        post_gp = np.nan
                    
                    try:
                        post_g = event.find("td", {"class":"postseason g"}).text.strip()
                    except:
                        post_g = np.nan
                    
                    try:
                        post_a = event.find("td", {"class":"postseason a"}).text.strip()
                    except:
                        post_a = np.nan
                    
                    try:
                        post_tp = event.find("td", {"class":"postseason tp"}).text.strip()
                    except:
                        post_tp = np.nan
                    
                    try:
                        post_pim = event.find("td", {"class":"postseason pim"}).text.strip()
                    except:
                        post_pim = np.nan
                    
                    try:
                        post_pm = event.find("td", {"class":"postseason pm"}).text.strip()
                    except:
                        post_pm = np.nan
                    
                    
                    row_df = pd.DataFrame({
                        "ep_id":[ep_id], "event_type":["tournament"],
                        "season":[season], "team":[team], "league":[league], "league_url":[league_url], "league_nation_code":[league_nation_code],
                        "reg_gp":[reg_gp], "reg_g":[reg_g], "reg_a":[reg_a], "reg_pts":[reg_tp], "reg_pim":[reg_pim], "reg_pm":[reg_pm],
                        "post_type":[post_type], "post_gp":[post_gp], "post_g":[post_g], "post_a":[post_a], "post_pts":[post_tp], "post_pim":[post_pim], "post_pm":[post_pm],
                        "date_retrieved":[today], "source":[url]
                    })
                    
                    sk_stats_df = pd.concat([sk_stats_df, row_df])
            except:
                print("--Tournament stats unavailable or not scraped")
                pass
            
            
        print("--Scrape successful!")
        time.sleep(25)
    
    except:
        time.sleep(5)
        print("--Player not scraped")
        missed_urls.append(url)
        pass




#%% SAVE PLAYER INFORMATION AND STATISTICS

# Save backup copies
old_info = pd.read_csv("Data/players/player_information.csv")
old_sk_stats = pd.read_csv("Data/players/skater_statistics.csv")
old_gl_stats = pd.read_csv("Data/players/goalie_statistics.csv")

old_info.to_csv("Data/players/player_information_backup.csv", index = False)
old_sk_stats.to_csv("Data/players/skater_statistics_backup.csv", index = False)
old_gl_stats.to_csv("Data/players/goalie_statistics_backup.csv", index = False)


# Remove accents
info_df["birthplace"] = info_df["birthplace"].apply(unidecode)
info_df["nation"] = info_df["nation"].apply(unidecode)
sk_stats_df["team"] = sk_stats_df["team"].astype(str).apply(unidecode)
sk_stats_df["league"] = sk_stats_df["league"].astype(str).apply(unidecode)
gl_stats_df["team"] = gl_stats_df["team"].astype(str).apply(unidecode)
gl_stats_df["league"] = gl_stats_df["league"].astype(str).apply(unidecode)
sk_stats_df["team"] = np.where(sk_stats_df["team"] == "nan", np.nan, sk_stats_df["team"])
sk_stats_df["league"] = np.where(sk_stats_df["league"] == "nan", np.nan, sk_stats_df["league"])
gl_stats_df["team"] = np.where(gl_stats_df["team"] == "nan", np.nan, gl_stats_df["team"])
gl_stats_df["league"] = np.where(gl_stats_df["league"] == "nan", np.nan, gl_stats_df["league"])

# Save updated data
info_df.to_csv("Data/players/player_information.csv", index = False)
sk_stats_df.to_csv("Data/players/skater_statistics.csv", index = False)
gl_stats_df.to_csv("Data/players/goalie_statistics.csv", index = False)



