#Sending automatic email
#from email import *
#tried pip installing this class, can't access the subprocesses, ask for help
import requests
from bs4 import BeautifulSoup
import json
import smtplib
import os
from datetime import date
from datetime import timedelta

#nba api
URL = "http://data.nba.net/10s/prod/v1"
#https://www.quora.com/Is-there-an-NBA-API-for-free-that-has-live-stats
def ReadUrl(url):
    #finds the website from the url
    page = requests.get(url)

    #pulling html from the page
    soup = BeautifulSoup(page.text, 'html.parser')
    soup = str(soup)

    return soup

#finds and formats yesterday's date so that I can find the correct directory
def yesterday():
    yesterday = date.today() - timedelta(days=1)
    yyear = str(yesterday.year)
    ymonth = str(yesterday.month)
    if(len(ymonth)== 1):
        ymonth = "0" + ymonth
    yday = str(yesterday.day)
    return yyear + ymonth + yday

#initiaing the email connection and logging in
#s = smtplib.SMTP('smtp.gmail.com', 587)
#s.ehlo()
#s.starttls()
#s.login('nbascores.py@gmail.com', 'rZwg2vAc')

#pulling the data from the api
#https://stackoverflow.com/questions/73028029/how-to-get-stats-games-of-a-specific-date-using-data-nba-net
#today's Scoreboard
FILE = "/20220410/scoreboard.json"

#finds the correct json extension
def find_file():
    return "/" + yesterday() + "/scoreboard.json"

def get_links(url, file):
    data = requests.get(url + file).json()
    #links = data['links']
    return data

def get_scores(url, links):
    scoreboard = links['currentScoreboard']
    games = requests.get(url + scoreboard).json()['games']
    scores = []
    for g in games:
        temp = ""
        home = g['hTeam']
        hscore = g[''] #Find the link for the scores
        away = g['vTeam']
        ascore = g[''] #find the link!!
        if(hscore > ascore):
            temp = home + ": " + hscore + "beat " + away + ": " + ascore
        else:
            temp = away + ": " + ascore + "beat " + home + ": " + hscore
        scores.append(temp)
    return scores



    
