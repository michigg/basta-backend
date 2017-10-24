import requests
from bs4 import BeautifulSoup
import json
import datetime
import re

SPEISEPLAN_NAME_SELECTOR = '.csc-default .csc-header .csc-firstHeader'


def loadPage(url: str):
    return requests.get(url).content


def getFoodplanName(soup):
    foodplan_name = soup.select(SPEISEPLAN_NAME_SELECTOR)[0].getText()
    return foodplan_name


def getRightLine(lines):
    foodlines = []
    pattern = re.compile("[0-9]+.+[A-Z]+")
    for line in list(lines):
        line = line.getText()
        if pattern.match(line):
            foodlines.append(line)
    return foodlines


def getFoodPerDay(soup):
    days = []
    lines = soup.select('.csc-default .bodytext')
    foodlines = getRightLine(lines)
    for food in foodlines:
        dayObj = {}
        day = str(food).split()[0]
        foodName = str(food).replace(day, "").strip()
        dayObj['date'] = day
        dayObj['menu'] = [foodName]
        days.append(dayObj)
    return days


def parsePage(url: str):
    pagecontent = {}
    # {mensaspeiseplan:
    #   {name:"",
    #    weekmenu: [day:{date:, menu:[,,,]}]
    #   }
    # }

    page = loadPage(url)
    mensaSpeiseplan = {}
    soup = BeautifulSoup(page, "lxml")
    foodplan_name = getFoodplanName(soup)

    days = getFoodPerDay(soup)
    mensaSpeiseplan['weekmenu'] = days
    mensaSpeiseplan['name'] = foodplan_name
    mensaSpeiseplan['execution_time'] = datetime.datetime.today().strftime("%A, %d.%m.%Y")
    mensaSpeiseplanJson = json.dumps(mensaSpeiseplan)
    return mensaSpeiseplanJson


# LINK_ERBA_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-erba-insel.html"
# parsePage(LINK_ERBA_CAFETE)
