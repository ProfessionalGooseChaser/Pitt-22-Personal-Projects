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
FILE = "/20220322/scoreboard.json"
def find_file():
    return "/" + yesterday() + "/scoreboard.json"

def get_data(url, file):
    data = requests.get(url + file).json()
    return data

def get_scores(data):
    gms = []
    for i in data['games']:
        gm = []
        #separates games, each i is a game

        #visting team info
        gm.append(i['vTeam']['triCode'])
        gm.append(i['vTeam']['win'])
        gm.append(i['vTeam']['loss'])
        gm.append(i['vTeam']['score'])

        gm.append(i['hTeam']['triCode'])
        gm.append(i['hTeam']['win'])
        gm.append(i['hTeam']['loss'])
        gm.append(i['hTeam']['score'])

        gms.append(gm)
    return gms


print('\n' * 5)
count = 0
for i in get_scores(get_data(URL, FILE)):
    print(i)
    print('\n')




#finding games in json file
#numgames: how many games were played that day
#gameid: there's a unique identifier for each game
#data from each game
#tri code (GSW for golden state warriors)
#Team Record
#Score
