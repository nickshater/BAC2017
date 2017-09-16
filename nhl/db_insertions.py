#-*- coding: utf-8 -*-
###############################################################################
# MODULE: db_insertions
# this is a repo of tools designed to create or update the graph db
# 
# Author:   BAC
# Created:  9.13.2017   
###############################################################################
import os
import pickle
from py2neo import Graph, Node

# open and reset the graph 
graph = Graph('bolt://45.77.104.192:7687',
              user_name ='neo4j',
              password  ='baltimoreAlgo')
graph.delete_all()

# insert team nodes
team_dict = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pickles','dict_names.pickle'),'rb'))
for k,v in team_dict.items():
    graph.create(Node("team",abbr=k,name=v))

# insert game nodes
games_df = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pickles','table_games.pickle'),'rb'))
for _,row in games_df.iterrows():
    node = Node("game", guid = row['guid'],
                        date = row['date'],
                        time = row['time'],
                        attendance = row['attendance'],
                        duration = row['duration'],
                        overtime = row['overtime'],
                        home_team = row['home_team'],
                        away_team = row['away_team'],
                        winner = row['winner'],
                        home_shots = row['home_shots'],
                        home_goals = row['home_goals'],
                        home_goals_pp = row['home_goals_pp'],
                        home_goals_sh = row['home_goals_sh'],
                        home_pen_min = row['home_pen_min'],
                        home_chances_pp = row['home_chances_pp'],
                        home_season_wins = row['home_season_wins'],
                        home_season_losses = row['home_season_losses'],
                        home_season_losses_ot = row['home_season_losses_ot'],
                        home_season_ties = row['home_season_ties'],
                        home_season_streak = row['home_season_streak'],
                        away_shots = row['away_shots'],
                        away_goals = row['away_goals'],
                        away_goals_pp = row['away_goals_pp'],
                        away_goals_sh = row['away_goals_sh'],
                        away_pen_min = row['away_pen_min'],
                        away_chances_pp = row['away_chances_pp'],
                        away_season_wins = row['away_season_wins'],
                        away_season_losses = row['away_season_losses'],
                        away_season_losses_ot = row['away_season_losses_ot'],
                        away_season_ties = row['away_season_ties'],
                        away_season_streak = row['away_season_streak'],
                        )
    graph.create(node)

# insert game-team relationships
graph.run("""
          MATCH (a:game), (b:team)
          WHERE a.home_team = b.abbr
          CREATE (a)<-[r:home]-(b)
          """)
graph.run("""
          MATCH (a:game),(b:team)
          WHERE a.away_team = b.abbr
          CREATE (a)<-[r:away]-(b)
          """)