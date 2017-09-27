import requests
import datetime
import xmltodict
import json


def loadPage(url: str):
    return requests.get(url).content


def getDay():
    return datetime.datetime.today().strftime("%A, %d.%m.%Y")


def parsePage(url: str):
    # {Univis: {'Event':[{,,,,},,,,]}}
    page = loadPage(url)
    dict = xmltodict.parse(page)
    json_data = json.dumps(dict)
    json_data = json.loads(json_data)
    json_data['last_execute'] = getDay()
    return json.dumps(json_data)

# UNIVIS_RPG_URL = "http://univis.uni-bamberg.de/prg?search=events&show=xml"
# parsePage(UNIVIS_RPG_URL)
