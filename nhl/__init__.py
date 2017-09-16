# -*- coding: utf-8 -*-

import os

import pickle

def print_teams():
    """
    return: list of teams
    """
    abbrevs = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pickles','dict_names.pickle'),'rb'))
    for k,v in abbrevs.items(): print(k + ": " + ','.join(v))

def team_given_abbrev(team_abbrev):
    """
    @param: abbreviation
    return: team name else none; case insensitive
    """
    abbrevs = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pickles','dict_names.pickle'),'rb'))
    return abbrevs.get(team_abbrev)

def abbrev_given_team(team_name):
    """
    @param: team name
    return: abbrev else none; case insensitive
    """
    abbrevs = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pickles','dict_names.pickle'),'rb'))
    names = {v: k for k, v in abbrevs.items()}
    out = names.get(team_name)
    if out==None: print("NOT FOUND: " + team_name)
    return out

#def seconds_given_time():
#    """
#    @param: time, e.g. '12:01'
#    return: seconds
#    """