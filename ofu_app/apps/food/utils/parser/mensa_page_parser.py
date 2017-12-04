import requests
from bs4 import BeautifulSoup
import json
import datetime


# FEKI_URL = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=3&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=c3fe5ebb35e5fba3794f01878e798b7c"


def loadPage(url: str):
    return requests.get(url).content


def getMenuDay(soup):
    return soup.find("div", {"class": "day"}).h5.contents[0]


def getFoodPerDay(soup):
    week_menus = []
    for day in soup.select('.currentweek .day'):
        menu = {}
        daysoup = BeautifulSoup(str(day), "lxml")
        day = getMenuDay(daysoup)
        day_menu = []
        for singleFood in daysoup.select('.menuwrap .menu'):
            singleFoodObj = {}
            singleFoodSoup = BeautifulSoup(str(singleFood), "lxml")
            title = singleFoodSoup.find('div', {'class': 'title'}).getText()
            allergens = [e.getText() for e in singleFoodSoup.select('.left .additnr .toggler ul li')]
            prices = {}
            if singleFoodSoup.select('.price'):
                prices['price_student'] = singleFoodSoup.select('.price')[0]['data-default']
            if singleFoodSoup.select('.price'):
                prices['price_employee'] = singleFoodSoup.select('.price')[0]['data-bed']
            if singleFoodSoup.select('.price'):
                prices['price_guest'] = singleFoodSoup.select('.price')[0]['data-guest']
            singleFoodObj['title'] = title
            singleFoodObj['allergens'] = allergens
            singleFoodObj['prices'] = prices
            day_menu.append(singleFoodObj)

        menu['date'] = str(day).split(" ")[1]
        menu['menu'] = day_menu
        week_menus.append(menu)
    return week_menus


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
    mensaSpeiseplanJson = json.dumps(mensaSpeiseplan)
    return mensaSpeiseplanJson


def getFoodplanName(soup):
    foodplan_name = soup.select('.mensamenu h2')[0].getText()
    return foodplan_name

# parsePage(FEKI_URL)
