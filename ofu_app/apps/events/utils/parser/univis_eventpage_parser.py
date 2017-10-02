import requests
import datetime
import xmltodict
import json

# CONFIG
UNIVIS_RPG_URL = "http://univis.uni-bamberg.de/prg?search=events&show=xml"


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


def parsePage():
    # {Univis: {'Event':[{,,,,},,,,]}}
    page = loadPage(UNIVIS_RPG_URL)
    dict = xmltodict.parse(page)
    # resolveUnivisRefs(dict)
    json_data = json.dumps(dict)
    json_data = json.loads(json_data)
    resolveDates(json_data)
    json_data['last_execute'] = getDay()
    return json.dumps(json_data)

# parsePage()
