import requests
import datetime
import xmltodict
import json
from pprint import pprint

# CONFIG
UNIVIS_RPG_GuK = "http://univis.uni-bamberg.de/prg?search=rooms&department=Fakult%E4t%20Geistes-%20und%20Kulturwissenschaften&show=xml"
UNIVIS_RPG_SoWi = "http://univis.uni-bamberg.de/prg?search=rooms&department=Fakult%E4t%20Sozial-%20und%20Wirtschaftswissenschaften&show=xml"
UNIVIS_RPG_HuWi = "http://www.config.de/cgi-bin/prg-wizard.pl"
UNIVIS_RPG_WIAI = "http://univis.uni-bamberg.de/prg?search=rooms&department=Fakult%E4t%20Wirtschaftsinformatik&show=xml"


def loadPage(url: str):
    return requests.get(url).content


def getDay():
    return datetime.datetime.today().strftime("%A, %d.%m.%Y")


def getRoom(dict: dict):
    rooms = []
    for room in dict['UnivIS']['Room']:
        rooms.append(room)
    return rooms


def parsePage(url):
    page = loadPage(url)
    dict = xmltodict.parse(page)
    rooms = getRoom(dict)
    return rooms

# parsePage()
