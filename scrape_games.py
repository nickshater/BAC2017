# -*- coding: utf-8 -*-
###############################################################################
# MODULE: scrape games
#
# Author:   BAC
# Created:  09.14.2017
###############################################################################

import re
import os
import time
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm
from random import random
from bs4 import BeautifulSoup
from urllib.request import urlopen

import nhl

"""
1. Pulls dictionary of team names
2. Scrapes all games for all teams for all years >= 2000
3. Preprocesses data and dumps into pickled dataframe
NOTE: games are merged in a poor way, but seems to work just fine.
"""
#iterate over teams/years
teams = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'nhl','pickles','dict_names.pickle'),'rb'))
years = range(2000,2018)

# start loop
all_data = [];
for team in teams:
    for year in tqdm(years):
    
        # IF site exists THEN scrape headers and table
        try:
            url = 'https://www.hockey-reference.com/teams/' + team + '/' + str(year) + '_games.html'
            soup = BeautifulSoup(urlopen(url),'lxml')
            full_table = soup.find("div",{"id":"all_games"})
            headers = full_table.find('thead')
            headers = headers.findAll('tr')[1]
            headers = [i['data-stat'].lower() for i in headers.find_all('th')]
            table = full_table.find('tbody')
        except: continue

        # build table
        data = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            cols = [m.text.strip() for m in cols]
            if cols: data.append([team] + [m for m in cols])
        data = pd.DataFrame(data,columns=headers)
    		
        # dump headers with 'empty' in them
        for i in headers:
            if 'empty' in i: data = data.drop(i,1)
        
        # replace opponent name with abbreviation
        data['opp_name'] = [nhl.abbrev_given_team(i) for i in data['opp_name']]
        all_data.append(data)
        
        # pause for scraping courtesy
        time.sleep(0.5*float(random()))

# drop bad columsns, rename initial columns
df = pd.concat(all_data)
df = df.drop('game_remarks',1)    # delete useless column (location if changed, uncommon)
df = df[df.game_outcome != '']    # delete games with no outcome (postponed games)
df.rename(columns={'games':'team_1'},inplace=True)           # rename for code readability
df.rename(columns={'opp_name':'team_2'},inplace=True)        # rename for code readability

# rename for clarity/consistancy
df.rename(columns={'date_game':'date'},inplace=True)
df.rename(columns={'time_game':'time'},inplace=True)
df.rename(columns={'game_duration':'duration'},inplace=True)
df.rename(columns={'overtimes':'overtime'},inplace=True)
df.rename(columns={'game_outcome':'winner'},inplace=True)

# data needs to be reassigned to be "home_ vs away_" instead of "team_1 vs team_2"
df["guid"] = ""

df["home_team"] = ""
df["away_team"] = ""

df['home_shots'] = ""
df['home_goals'] = ""
df['home_goals_pp'] = ""
df['home_goals_sh'] = ""
df['home_pen_min'] = ""
df['home_chances_pp'] = ""
df['home_season_wins'] = ""
df['home_season_losses'] = ""
df['home_season_losses_ot'] = ""
df['home_season_ties'] = ""
df['home_season_streak'] = ""

df['away_shots'] = ""
df['away_goals'] = ""
df['away_goals_pp'] = ""
df['away_goals_sh'] = ""
df['away_pen_min'] = ""
df['away_chances_pp'] = ""
df['away_season_wins'] = ""
df['away_season_losses'] = ""
df['away_season_losses_ot'] = ""
df['away_season_ties'] = ""
df['away_season_streak'] = ""

# iterate and move data to appropriate fields
for _,row in df.iterrows():    
			
	# IF game_location=="" THEN team_1 is home, else team_2 is home game_location="@"s    
	if row['game_location']=="":
		row['home_team'] = row['team_1']
		row['away_team'] = row['team_2']        

		row['home_shots'] =             row['shots']
		row['home_goals'] =             row['goals']
		row['home_goals_pp'] =          row['goals_pp']
		row['home_goals_sh'] =          row['goals_sh']
		row['home_pen_min'] =           row['pen_min']
		row['home_chances_pp'] =        row['chances_pp']
		row['home_season_wins'] =       row['wins']
		row['home_season_losses'] =     row['losses']
		row['home_season_losses_ot'] =  row['losses_ot']
		row['home_season_ties'] =       row['ties']
		row['home_season_streak'] =     row['game_streak']
	elif row['game_location']=="@":
		row['home_team']=row['team_2']
		row['away_team']=row['team_1']

		row['away_shots'] =             row['shots']
		row['away_goals'] =             row['goals']
		row['away_goals_pp'] =          row['goals_pp']
		row['away_goals_sh'] =          row['goals_sh']
		row['away_pen_min'] =           row['pen_min']
		row['away_chances_pp'] =        row['chances_pp']
		row['away_season_wins'] =       row['wins']
		row['away_season_losses'] =     row['losses']
		row['away_season_losses_ot'] =  row['losses_ot']
		row['away_season_ties'] =       row['ties']
		row['away_season_streak'] =     row['game_streak']
	else: raise Exception("Incorrect game indicator detected. Aborting.")
	
	# define game guid (YYYYMMDD + 0 + home_team)
	row['guid'] = re.sub('-','',row['date']) + '0' + row['home_team']
	
	# place winning team into game_outcome/winner column
	if row["winner"]=='W':     row["winner"]=row['team_1'] # win
	elif row["winner"]=='L':   row["winner"]=row['team_2'] # lose
	elif row["winner"]=='T':   row["winner"]="T"           # tie
	else: raise Exception("Incorrect win/lost/tie indicator detected. Aborting.")
	
# delete old headers and reorder
df = df.sort_values('date')
df = df.drop('game_location',1)
df = df.drop(['shots','goals','goals_pp','goals_sh','pen_min','chances_pp','wins','losses','losses_ot','ties','game_streak'],1)
headers = ['guid','date','time','attendance','duration','overtime','home_team','away_team','winner','home_shots','home_goals','home_goals_pp','home_goals_sh','home_pen_min','home_chances_pp','home_season_wins','home_season_losses','home_season_losses_ot','home_season_ties','home_season_streak','away_shots','away_goals','away_goals_pp','away_goals_sh','away_pen_min','away_chances_pp','away_season_wins','away_season_losses','away_season_losses_ot','away_season_ties','away_season_streak']
df = df[headers]
df = df.sort_values('date')
df = df.reset_index(drop=True)

# THIS IS A POOR WAY OF DOING THIS (merge home/away game instances into single instance)
# better approach to implement later:
# 1. build dict where key = guid; val = pandas series
# 2. dump in all key/values
# 3. optionaly build back into table for dumping into db
df = df.replace(np.nan,'NULL')
df = df.replace('',np.nan)
i=0
while i<df.shape[0]-1:
	a = df.loc[df.index[i]][0:9]
	j=i+1
	while j<df.shape[0]:
		b = df.loc[df.index[j]][0:9]
		if a.equals(b):
			df.loc[df.index[i]] = df.loc[df.index[i]].fillna(df.loc[df.index[j]])
			df = df.drop(df.index[j])
			break
		j+=1
	if j==df.shape[0]-1: print(df.loc[df.index[i]])
	i+=1
df = df.replace('-','')
df = df.replace(np.nan,'')
df = df.sort_values('date')
df = df.reset_index(drop=True)

# dump the dataframe into a pickle
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'nhl','pickles','table_games.pickle'),'wb') as f:
    pickle.dump(df,f)