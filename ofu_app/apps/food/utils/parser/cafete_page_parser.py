import requests
from bs4 import BeautifulSoup
import json
import datetime

SPEISEPLAN_NAME_SELECTOR = '.csc-default .csc-header .csc-firstHeader'


def loadPage(url: str):
    return requests.get(url).content


def getFoodplanName(soup):
    foodplan_name = soup.select(SPEISEPLAN_NAME_SELECTOR)[0].getText()
    return foodplan_name


def getRightLine(lines):
    for line in list(lines):
        if str(line).__contains__("<br/>"):
            return line
    return ""


def getFoodPerDay(soup):
    days = []
    lines = soup.select('.csc-default .bodytext')
    line = getRightLine(lines)
    foods = str(line).strip('<p class="bodytext">').strip('</').split("<br/>")
    for food in foods:
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
