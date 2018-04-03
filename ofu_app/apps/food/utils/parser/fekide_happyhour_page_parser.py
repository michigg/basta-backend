import datetime
import logging

from bs4 import BeautifulSoup

from . import load_page

logger = logging.getLogger(__name__)

SPEISEPLAN_NAME_SELECTOR = '.csc-default .csc-header .csc-firstHeader'


def get_day():
    return datetime.datetime.today().strftime("%A, %d.%m.%Y")


def get_happy_hours(soup):
    happyhours = []
    happyhourstable = soup.select('#food .table tr')
    for tableline in happyhourstable:
        linesoup = BeautifulSoup(str(tableline), "lxml")
        location = linesoup.find("td", {"class": "location"}).getText()
        time = linesoup.find("td", {"class": "time"}).getText()
        description = linesoup.find("td", {"class": "description"}).getText()
        description = str(description).strip()
        happyhour = {
            'location': location,
            'time': time,
            'description': description
        }
        happyhours.append(happyhour)
    return happyhours


def parse_page(url: str):
    # {
    # happyhours:[{happyhour:{location: "",time: "",description: ""},,,,]
    # }
    happyhours = []
    try:
        page = load_page(url)
        soup = BeautifulSoup(page, "lxml")
        happyhours = get_happy_hours(soup)
        return {
            'happyhours': happyhours,
            'day': get_day(),
            'execution_time': datetime.datetime.today().strftime("%A, %d.%m.%Y")
        }
    except Exception as e:
        logger.exception(e)
    return None
# LINK_FEKIDE_GUIDE = "https://www.feki.de/happyhour/wochenuebersicht"
# parsePage(LINK_FEKIDE_GUIDE)
