import requests
import datetime
import xmltodict
import json
from pprint import pprint


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
