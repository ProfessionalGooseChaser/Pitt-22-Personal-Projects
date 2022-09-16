#Sending automatic email
#Uses a screen scraper and the data.nba.net api to send me daily emails of the nba scores from the night previous


#https://www.geeksforgeeks.org/how-to-send-automated-email-messages-in-python/ ~ Sending automatic emails
#https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/ ~ sending emails with python

#from email.mine.text import MINEText
#from email.mine.image import MINEImage
#from email.mine.multipart import MINEMultipart

#tried pip installing this class, can't access the subprocesses
#have setuptools, and the most recent version of pip already installed

import requests
from bs4 import BeautifulSoup
import json
import smtplib
import os
from datetime import date
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont

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
FILE = "/20220410/scoreboard.json"
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

#create a dictionary with the tricodes of each team and a picture of their logo
#pictures have different aspect ratios, find a way to scale them without losing their aspect ratio

#the logos below usually include the team name... we can find different pngs so that we add the names ourselves or just add the names anyway
NBAdict = {
    "GSW" : ["Golden State Warriors", "GSW.png"],
    "BOS" : ["Boston Celtics", "BOS.png"],
    "LAL" : ["Los Angeles Lakers", "LAL.png"],
    "BKN" : ["Brooklyn Nets", "BKN.png"],
    "ATL" : ["Atlanta Hawks", "ATL.png"],
    "MIL" : ["Milwaukee Bucks", "MIL.png"],
    "CHI" : ["Chicago Bulls", "CHI.png"],
    "DET" : ["Detroit Pistons", "DET.png"],
    "DAL" : ["Dallas Mavericks", "DAL.png"],
    "WAS" : ["Washington Wizards", "WAS.png"],
    "NYK" : ["New York Knicks", "NYK.png"],
    "NOP" : ["New Orleans Pelicans", "NOP.png"],
    "PHI" : ["Philidelphi 76ers", "PHI.png"],
    "TOR" : ["Toronto Raptors", "TOR.png"],
    "MIA" : ["Miami Heat", "MIA.png"], 
    "CLE" : ["Cleveland Cavaliers", "CLE.png"],
    "MEM" : ["Memphis Grizzlies", "MEM.png"],
    "PHX" : ["Pheonix Suns", "PHX.png"],
    "OKC" : ["Oklahoma City Thunder", "OKC.png"],
    "SAS" : ["San Antonio Spurs", "SAS.png"],
    "MIN" : ["Minnesota Timberwolves", "MIN.png"],
    "UTA" : ["Utah Jazz", "UTA.png"],
    "SAC" : ["Sacremento Kings", "SAC.png"],
    "HOU" : ["Houston Rockets", "HOU.png"],
    "LAC" : ["Los Angeles Clippers", "LAC.png"],
    "ORL" : ["Orlando Magic", "ORL.png"],
    "POR" : ["Portland Trailblazers", "POR.png"],
    "DEN" : ["Denver Nuggets", "DEN.png"],
    "CHA" : ["Charlotte Hornets", "CHA.png"],
    "IND" : ["Indiana Pacers", "IND.png"]
}

def create_graphic(games):
    #creates an off-white background of 720 x 720  pixels
    WIDTH = 720
    bg = Image.new('RGB', (WIDTH, len(games) * 200), color= (245, 245, 245))
    count = 0
    for i in games:
        center = (count * 200)
        h_logo = Image.open(resize(NBAdict[i[0]][1])) #hteam logo
        bg.paste(h_logo, (center + 36, 36), h_logo)

        #add team name
        #add team record
        #won/lost
        #score
        #to
        
        v_logo = Image.open(resize(NBAdict[i[4]][1])) # vteam logo
        bg.paste(v_logo, (center + 36, WIDTH/2 + 36), h_logo) #may need to adjust this y value
        #add team name
        #add team record

        count += 1
    
    bg.save(yesterday() + ".png")

def resize(img):
    return img.thumbnail((128, 128))


#print(len(NBAdict))