# -*- coding: utf-8 -*-
###############################################################################
# MODULE: scrape player-game data
#
# Author:   BAC
# Created:  09.14.2017
# [INCOMPLETE]
###############################################################################
import os
import time
import pickle
import pandas as pd
from tqdm import tqdm
from random import random
from bs4 import BeautifulSoup
from urllib.request import urlopen

"""
1. Pulls dictionary of games
2. Scrape nodal information for all players for each game
3. Preprocesses data and dump into pickled dataframe
"""
 
# function to convert html table to a custom pandas dataframe
def build_table(html_table,headers,guid,date,team,home_or_away):
    data = []
    table = html_table.find('tbody')
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        cols = [m.text.strip() for m in cols]
        if cols: data.append([guid] + [date] + [team] + [home_or_away] + [m for m in cols])
    data = pd.DataFrame(data,columns=headers)
    return data

# loop for all games
games = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'nhl','pickles','table_games.pickle'),'rb'))
skaters = []
goalies = []
not_found = []
progress = tqdm(total = games.shape[0])
counter = 0
for _,row in games.iterrows():
    counter+=1
    progress.update()
    guid = row['guid']
    date = row['date']
    home_team = row['home_team']
    away_team = row['away_team']
    
    # IF site exists THEN scrape headers and table
    try:
        url = 'https://www.hockey-reference.com/boxscores/' + row['guid'] + '.html'
        soup = BeautifulSoup(urlopen(url),'lxml')
    except:
        not_found.append(url)
        print("URL not found: " + url)
        continue
        
    # get html tables
    home_skaters = soup.find("div",{"id":'all_' + home_team + '_skaters'})
    home_goalies = soup.find("div",{"id":'all_' + home_team + '_goalies'})
    away_skaters = soup.find("div",{"id":'all_' + away_team + '_skaters'})
    away_goalies = soup.find("div",{"id":'all_' + away_team + '_goalies'})
    if not all([home_skaters,home_goalies,away_skaters,away_goalies]):
        not_found.append(url)
        print("Data missing: " + url)
    
    # get headers
    headers_skaters = home_skaters.find('thead').findAll('tr')[1]
    headers_skaters = [i['data-stat'].lower() for i in headers_skaters.find_all('th')]
    headers_goalies = home_goalies.find('thead').findAll('tr')[1]
    headers_goalies = [i['data-stat'].lower() for i in headers_goalies.find_all('th')]
    
    headers_skaters.remove('ranker')
    headers_skaters = ['guid','date','team','home_away'] + headers_skaters
    headers_goalies.remove('ranker')
    headers_goalies = ['guid','date','team','home_away'] + headers_goalies    
    
    # build dataframes from html
    df_home_skaters = build_table(home_skaters,headers_skaters,guid,date,home_team,'home')
    df_home_goalies = build_table(home_goalies,headers_goalies,guid,date,home_team,'home')
    df_away_skaters = build_table(away_skaters,headers_skaters,guid,date,away_team,'away')
    df_away_goalies = build_table(away_goalies,headers_goalies,guid,date,away_team,'away')
    
    # replace opponent name with abbreviation
    skaters.append(df_home_skaters)
    skaters.append(df_away_skaters)
    goalies.append(df_home_goalies)
    goalies.append(df_away_goalies)
    
    # pause for scraping courtesy
    #time.sleep(0.5*float(random()))
    
    # save every 20 runs
    if counter%20==0:
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'nhl','pickles','table_players.pickle'),'wb') as f:
                pickle.dump(skaters,f)
                pickle.dump(goalies,f)
                pickle.dump(not_found,f)
                pickle.dump(row,f)

# pandas dataframe cleanup and pickle dump
progress.close()
df_skaters = pd.concat(skaters)
df_skaters = df_skaters.sort_values('guid')
df_skaters = df_skaters.reset_index(drop=True)
df_skaters = df_skaters.replace('','NULL')
df_goalies = pd.concat(goalies)
df_goalies = df_goalies.sort_values('guid')
df_goalies = df_skaters.reset_index(drop=True)
df_goalies = df_goalies.replace('','NULL')

