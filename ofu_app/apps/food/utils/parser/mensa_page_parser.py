import datetime
import logging

from bs4 import BeautifulSoup

from . import load_page

logger = logging.getLogger(__name__)


def getMenuDay(soup):
    return soup.find("div", {"class": "day"}).h5.contents[0]


def getFoodPerDay(soup):
    week_menus = []
    for day in soup.select('.currentweek .day'):
        daysoup = BeautifulSoup(str(day), "lxml")
        day = getMenuDay(daysoup)
        day_menu = []
        for singleFood in daysoup.select('.menuwrap .menu'):
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
            single_food_obj = {
                'title': title,
                'allergens': allergens,
                'prices': prices
            }
            logger.debug('Title: {}'.format(title))
            logger.debug('Allergens: {}'.format(allergens))
            logger.debug('Price: {}'.format(prices))
            day_menu.append(single_food_obj)

        date = str(day).strip('<span>').strip('</span>').split(" ")[1]
        logger.debug('Date: {}'.format(date))
        menu = {
            'date': date,
            'menu': day_menu
        }
        week_menus.append(menu)
    return week_menus


def parsePage(url: str):
    pagecontent = {}
    # {mensaspeiseplan:
    #   {name:"",
    #    weekmenu: [day:{date:, menu:[,,,]}]
    #   }
    # }
    try:
        page = load_page(url)
        soup = BeautifulSoup(page, "lxml")
        foodplan_name = getFoodplanName(soup)
        days = getFoodPerDay(soup)
        return {
            'weekmenu': days,
            'name': foodplan_name,
            'execution_time': datetime.datetime.today().strftime("%A, %d.%m.%Y")
        }
    except Exception as e:
        logger.exception(e)
    return None


def getFoodplanName(soup):
    foodplan_name = soup.select('.mensamenu h2')[0].getText()
    return foodplan_name

# parsePage(FEKI_URL)
