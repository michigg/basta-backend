import requests
from bs4 import BeautifulSoup
import datetime
import json

SPEISEPLAN_NAME_SELECTOR = '.csc-default .csc-header .csc-firstHeader'


def loadPage(url: str):
    return requests.get(url).content


def getDay():
    return datetime.datetime.today().strftime("%A, %d.%m.%Y")


def getHappyHours(soup):
    happyhours = []
    happyhourstable = soup.select('#food .table tr')
    for tableline in happyhourstable:
        happyhour = {}
        linesoup = BeautifulSoup(str(tableline), "lxml")
        location = linesoup.find("td", {"class": "location"}).getText()
        time = linesoup.find("td", {"class": "time"}).getText()
        description = linesoup.find("td", {"class": "description"}).getText()
        description = str(description).strip()

        happyhour['location'] = location
        happyhour['time'] = time
        happyhour['description'] = description
        happyhours.append(happyhour)
    return happyhours


def parsePage(url: str):
    pagecontent = {}
    # {
    # happyhours:[{happyhour:{location: "",time: "",description: ""},,,,]
    # }
    happyhours = []

    page = loadPage(url)
    soup = BeautifulSoup(page, "lxml")
    happyhours = getHappyHours(soup)
    pagecontent['happyhours'] = happyhours
    pagecontent['day'] = getDay()
    pagecontent['execution_time'] = datetime.datetime.today().strftime("%A, %d.%m.%Y")

    jsondata = json.dumps(pagecontent)
    return jsondata

# LINK_FEKIDE_GUIDE = "https://www.feki.de/happyhour/wochenuebersicht"
# parsePage(LINK_FEKIDE_GUIDE)
