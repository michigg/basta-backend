import requests
import datetime
import xmltodict
from pprint import pprint
import json

# CONFIG
UNIVIS_RPG_GuK = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Geistes-%20und%20Kulturwissenschaften&show=xml"
UNIVIS_RPG_SoWi = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Sozial-%20und%20Wirtschaftswissenschaften&show=xml"
UNIVIS_RPG_HuWi = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Humanwissenschaften&show=xml"
UNIVIS_RPG_WIAI = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Wirtschaftsinformatik&show=xml"


def loadPage(url: str):
    return requests.get(url).content


def getDay():
    return datetime.datetime.today().strftime("%A, %d.%m.%Y")


def getRoom(dict: dict, id: str):
    for room in dict['UnivIS']['Room']:
        if room['@key'] == id:
            return room


def resolveUnivisRefs(dict: dict):
    for event in dict['UnivIS']['Event']:
        if 'rooms' in event:
            room = event['rooms']['room']
            if 'UnivISRef' in room:
                key = room['UnivISRef']['@key']
                detailed_room = getRoom(dict, key)
                event['rooms']['room'] = detailed_room


def resolveDates(json):
    for event in json['UnivIS']['Event']:
        start_datetime = datetime.datetime.strptime(event['startdate'], "%Y-%m-%d").strftime("%d.%m.%Y")
        event['startdate'] = start_datetime
        end_datetime = datetime.datetime.strptime(event['enddate'], "%Y-%m-%d").strftime("%d.%m.%Y")
        event['enddate'] = end_datetime


def getEvents(dict):
    events = []
    for event in dict['UnivIS']['Event']:
        events.append(event)
    return events


def getRooms(dict: dict):
    rooms = []
    for room in dict['UnivIS']['Room']:
        rooms.append(room)
    return rooms


def getPersons(dict: dict):
    persons = []
    for person in dict['UnivIS']['Person']:
        persons.append(person)
    return persons


def parsePage(url):
    page = loadPage(url)
    dict = xmltodict.parse(page)
    return getEvents(dict), getRooms(dict), getPersons(dict)

# parsePage(UNIVIS_RPG_GuK)
