import requests
from bs4 import BeautifulSoup
import datetime
import json
from pprint import pprint
import os
import locale

SPEISEPLAN_NAME_SELECTOR = '.csc-default .csc-header .csc-firstHeader'
LINK_FEKIDE_Events = "https://www.feki.de/terminkalender"
LINK_FEKIDE = "https://www.feki.de"

locale.setlocale(locale.LC_TIME, 'de_DE.utf-8')


def loadPage(url: str):
    return requests.get(url).content


def getDay():
    return datetime.datetime.today().strftime("%A, %d.%m.%Y")


def getEvents(soup):
    datelist_json = []
    datelist = soup.select('#feki_terminkalender_overview .event_overview_day')
    for dateelement in datelist:
        date = {}
        datesoup = BeautifulSoup(str(dateelement), "lxml")
        date['date'] = datetime.datetime.strptime(datesoup.find('h3').getText(), "%d. %B").replace(
            year=datetime.datetime.now().year).strftime("%d.%m.%Y")
        events = datesoup.select('div a')
        events_arr = []
        for event_elem in events:
            event = {}
            eventsoup = BeautifulSoup(str(event_elem), "lxml")
            title_category = eventsoup.find('div', {'class': 'event_overview_title'})
            event['title'] = title_category.getText()
            event['category'] = title_category.find('span').getText()
            event['location'] = eventsoup.find('div', {'class': 'event_overview_location'}).getText()
            event['time'] = eventsoup.find('div', {'class': 'event_overview_time'}).getText()
            event['link'] = LINK_FEKIDE + event_elem['href']
            events_arr.append(event)
        date['events'] = events_arr
        datelist_json.append(date)
    return datelist_json


def getNextPage(soup):
    return soup.select('#block-system-main .pagination .next a')


def getAllDates(url: str):
    page = loadPage(url)
    soup = BeautifulSoup(page, "lxml")
    dates = getEvents(soup)
    nextPage = getNextPage(soup)
    dates_nextPage = []
    if nextPage:
        dates_nextPage = getAllDates(LINK_FEKIDE_Events + str(nextPage[0]['href']))
    return dates + dates_nextPage


def parsePage():
    pagecontent = {}
    pagecontent['dates'] = getAllDates(LINK_FEKIDE_Events)
    jsondata = json.dumps(pagecontent)
    return jsondata

# parsePage()
