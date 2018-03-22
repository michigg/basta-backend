import datetime
import logging
import re

from bs4 import BeautifulSoup

from . import load_page

logger = logging.getLogger(__name__)

SPEISEPLAN_NAME_SELECTOR = '.csc-default .csc-header .csc-firstHeader'


def get_foodplan_name(soup):
    foodplan_name = soup.select(SPEISEPLAN_NAME_SELECTOR)[0].getText()
    return foodplan_name


def get_right_line(lines):
    foodlines = []
    pattern = re.compile("[0-9]+.+[A-Z]+")
    for line in list(lines):
        line = line.getText()
        if pattern.match(line):
            foodlines.append(line)
    return foodlines


def get_food_per_day(soup):
    days = []
    lines = soup.select('.csc-default .bodytext')
    foodlines = get_right_line(lines)
    for food in foodlines:
        day = str(food).split()[0]
        food_name = str(food).replace(day, "").strip()
        single_food_obj = {'title': food_name}
        day_obj = {
            'date': day,
            'menu': [single_food_obj]
        }
        days.append(day_obj)
    return days


def parse_page(url: str):
    pagecontent = {}
    # {mensaspeiseplan:
    #   {name:"",
    #    weekmenu: [day:{date:, menu:[,,,]}]
    #   }
    # }
    try:
        page = load_page(url)
        soup = BeautifulSoup(page, "lxml")
        foodplan_name = get_foodplan_name(soup)

        days = get_food_per_day(soup)
        return {
            'weekmenu': days,
            'name': foodplan_name,
            'execution_time': datetime.datetime.today().strftime("%A, %d.%m.%Y")
        }
    except Exception as e:
        logger.exception(e)
    return None

# LINK_ERBA_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-erba-insel.html"
