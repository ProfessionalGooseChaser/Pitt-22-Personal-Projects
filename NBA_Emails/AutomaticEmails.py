#Sending automatic email
#Uses a screen scraper and the data.nba.net api to send me daily emails of the nba scores from the night previous


#https://www.geeksforgeeks.org/how-to-send-automated-email-messages-in-python/ ~ Sending automatic emails
#https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/ ~ sending emails with python

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import requests
from bs4 import BeautifulSoup
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
    yesterday = date.today() - timedelta(days=2)
    yyear = str(yesterday.year)
    ymonth = str(yesterday.month)
    if(len(ymonth)== 1):
        ymonth = "0" + ymonth
    yday = str(yesterday.day)
    return yyear + ymonth + yday

#initiaing the email connection and logging in

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
        gm.append(i['vTeam']['triCode'])    #0
        gm.append(i['vTeam']['win'])        #1
        gm.append(i['vTeam']['loss'])       #2
        gm.append(i['vTeam']['score'])      #3

        gm.append(i['hTeam']['triCode'])    #4
        gm.append(i['hTeam']['win'])        #5
        gm.append(i['hTeam']['loss'])       #6
        gm.append(i['hTeam']['score'])      #7

        gms.append(gm)
    return gms



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
    #creates an off-white background of 720 x ___ pixels
    WIDTH = 720
    bgO = Image.new('RGB', (WIDTH, len(games) * 200), color= (245, 245, 245))
    count = 0
    bg = ImageDraw.Draw(bgO)
    FONT = ImageFont.truetype("Monaco.ttf", 10)

    for i in games:
        print(i)
        center = (count * 200)
        h_logo = resize(NBAdict[i[0]][1]) #hteam logo
        width1, height1 = h_logo.size
        bgO.paste(h_logo, (int((160 - width1)/2), int(center + height1/2)))

        v_logo = resize(NBAdict[i[4]][1]) # vteam logo
        width2, height2 = v_logo.size
        bgO.paste(v_logo, (int((320 + width2 + WIDTH/2)/2), int(center + height2/2)))


        bg.text((160, center + 100), NBAdict[i[0]][0], fill="black", font = FONT) #add team name
        bg.text((200, center + 125), WL_record(i, True), fill = "black", font = FONT)#add team record
        if(i[3] > i[7]):#won/lost
            bg.text((290, center + 100), "Won", fill = "black", font = FONT)
        else:
            bg.text((290, center + 100), "Lost", fill = "black", font = FONT)

        bg.text((320, center + 100), findScore(i) + " to", fill = "black", font = FONT) # the score
        
        
        #may need to adjust this y value
        bg.text((WIDTH/2 + 190, center + 100), NBAdict[i[4]][0], fill="black", font = FONT)#add team name
        bg.text((WIDTH/2 + 230, center + 125), WL_record(i, False), fill = "black", font = FONT)#add team record
        
        count += 1
    
    bgO.show()
    bgO.save(str(yesterday()) + ".png")
    

def resize(IMAGE):
    img = Image.open("NBA_Logos/" + IMAGE)
    img.thumbnail((128, 128))
    return img

def WL_record(game, HorA):
    if(HorA):
        return str(game[1]) + " - " + str(game[2])
    else:
        return str(game[5]) + " - " + str(game[6])

def findScore(game):
    return str(game[3]) + " - " + str(game[7])
    
#create_graphic(get_scores(get_data(URL, FILE)))

#print(get_scores(get_data(URL, find_file())))

#print(len(NBAdict))

#initializing the connection to the server
sender = 'nbascores.py@gmail.com'

s = smtplib.SMTP('smtp.gmail.com', 587)
s.ehlo()
s.starttls()

#logging into my gmail
password = 'fuqwmuapsoicaqci'
s.login(sender, password)

#https://www.geeksforgeeks.org/how-to-send-automated-email-messages-in-python/
def message(subject = "", text = "", img = str(yesterday()) + '.png'):
    
    #initializes the email
    msg = MIMEMultipart()

    #writes the subject
    msg['Subject'] = subject

    #adds text (there shouldn't be any)
    msg.attach(MIMEText(text))

    create_graphic(get_scores(get_data(URL, FILE)))

    img_data = open(img, 'rb').read()
    msg.attach(MIMEImage(img_data)) #I shouldn't need to save and then open again. I did in fact have to save and reopen again

    return msg

#writes the message
DailyMail = message(yesterday())

#sends the message
MailingList = ['Cole.r.hansen22@gmail.com']
s.sendmail(from_addr=sender, to_addrs=MailingList, msg=DailyMail.as_string())

#breaks the connection to the server
s.quit()
