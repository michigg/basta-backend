import requests
from bs4 import BeautifulSoup
import json
import datetime

FEKI_URL = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=3&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=c3fe5ebb35e5fba3794f01878e798b7c"


def loadPage(url: str):
    return requests.get(url).content


def getMenuDay(soup):
    return soup.find("div", {"class": "day"}).h5.contents[0]


def getFoodPerDay(soup):
    days = []
    for day in soup.select('.currentweek .day'):
        dayObj = {}
        daysoup = BeautifulSoup(str(day), "lxml")
        day = getMenuDay(daysoup)
        dayMenu = [e.getText() for e in daysoup.select('.menuwrap .menu .left .title')]

        dayObj['date'] = str(day).split(" ")[1]
        dayObj['menu'] = dayMenu
        days.append(dayObj)
    return days


def parsePage(url: str):
    pagecontent = {}
    # {mensaspeiseplan:
    #   {name:"",
    #    weekmenu: [day:{date:, menu:[,,,]}]
    #   }
    # }
    mensaSpeiseplan = {}
    page = loadPage(url)
    soup = BeautifulSoup(page, "lxml")
    foodplan_name = getFoodplanName(soup)
    days = getFoodPerDay(soup)
    mensaSpeiseplan['weekmenu'] = days
    mensaSpeiseplan['name'] = foodplan_name
    mensaSpeiseplan['execution_time'] = datetime.datetime.today().strftime("%A, %d.%m.%Y")
    # print(mensaSpeiseplan)
    mensaSpeiseplanJson = json.dumps(mensaSpeiseplan)
    return mensaSpeiseplanJson


def getFoodplanName(soup):
    foodplan_name = soup.select('.mensamenu h2')[0].getText()
    return foodplan_name
# parsePage(FEKI_URL)
