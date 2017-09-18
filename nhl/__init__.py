# -*- coding: utf-8 -*-
"""
888b    888 888    888 888          .d88888b.  8888888b.  8888888b.   .d8888b.  
8888b   888 888    888 888         d88P" "Y88b 888  "Y88b 888  "Y88b d88P  Y88b 
88888b  888 888    888 888         888     888 888    888 888    888 Y88b.      
888Y88b 888 8888888888 888         888     888 888    888 888    888  "Y888b.   
888 Y88b888 888    888 888         888     888 888    888 888    888     "Y88b. 
888  Y88888 888    888 888         888     888 888    888 888    888       "888 
888   Y8888 888    888 888         Y88b. .d88P 888  .d88P 888  .d88P Y88b  d88P 
888    Y888 888    888 88888888     "Y88888P"  8888888P"  8888888P"   "Y8888P"  

A package for scraping and manipulating NHL data

AUTHOR: BAC
DATE:   2017-18

NOTES:  This __init__ file contains common information prints or string
        conversions for simple data wrangling. Check modules for other
        functionalities
"""
import os
import pickle
import oddscalculator as oc

########################### STRING CONVERSIONS ################################

def team_given_abbrev(team_abbrev):
    """
    @param: abbreviation
    return: team name else none; case insensitive
    """
    abbrevs = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pickles','dict_names'),'rb'))
    return abbrevs.get(team_abbrev)

def abbrev_given_team(team_name):
    """
    @param: team name
    return: abbrev else none; case insensitive
    """
    abbrevs = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pickles','dict_names'),'rb'))
    names = {v: k for k, v in abbrevs.items()}
    out = names.get(team_name)
    if out==None: print("NOT FOUND: " + team_name)
    return out

#def seconds_given_time():
#    """
#    @param: time, e.g. '12:01'
#    return: seconds
#    """

############################ ODDS CONVERSIONS #################################


############################ PRINT STATEMENTS #################################

def print_teams():
    abbrevs = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pickles','dict_names'),'rb'))
    for k,v in abbrevs.items(): print(k + ": " + v)

