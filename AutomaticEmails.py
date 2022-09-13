#Sending automatic email
from email import *
#tried pip installing this class, can't access the subprocesses, ask for help
import requests
from bs4 import BeautifulSoup
import json
import smtplib
import os

#nba api
url = "http://data.nba.net/10s/prod/v1/today.json"
#https://www.quora.com/Is-there-an-NBA-API-for-free-that-has-live-stats
def ReadUrl(url):
    #finds the website from the url
    page = requests.get(url)

    #pulling html from the page
    soup = BeautifulSoup(page.text, 'html.parser')
    soup = str(soup)

    return soup



#initiaing the email connection and logging in
s = smtplib.SMTP('smtp.gmail.com', 587)
s.ehlo()
s.starttls()
s.login('nbascores.py@gmail.com', 'rZwg2vAc')

#pulling the data from the api
#https://stackoverflow.com/questions/73028029/how-to-get-stats-games-of-a-specific-date-using-data-nba-net
