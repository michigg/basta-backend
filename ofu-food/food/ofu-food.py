#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import datetime

CSSFILE_WEB = "../css/bootstrap-4.0.0-beta-dist/css/bootstrap.css"

# thinkpad
# OUTPUTFILE = "../html/ofu-food.html"

# PI
OUTPUTFILE = "/media/data_1/www/pub-html/ofu-food.html"

LINK_FEKI_MENSA = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=3&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=c3fe5ebb35e5fba3794f01878e798b7c"
LINK_AUSTR_MENSA = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=2&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=511e047953ee1370c3b82c11a04624bb"
LINK_ERBA_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-erba-insel.html"
LINK_MARKUS_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-markusplatz.html"
LINK_FEKIDE_GUIDE = "https://www.feki.de/happyhour"


def getHtmlHeader():
    head = '<head>'
    head += '<meta charset="utf-8">'
    head += '<meta name="description" content="Sammelwebsite für das Essen der Uni Bamberg">'
    head += '<meta name="keywords" content="OFU, Otto-Friedrich, Universität, Bamberg">'
    head += '<link rel="stylesheet" href="' + CSSFILE_WEB + '">'
    head += '<title>Essen an der OFU</title>'
    head += '</head>'
    return head


def getExecuteTime():
    return "<p>Last execute: " + datetime.datetime.today().strftime("%d.%m.%Y") + "</p>"


def getFoodHtml(erbaHtml, markusHtml, austrHtml, fekiHtml, happyHourHtml):
    html = '<!doctype html>'
    html += '<html lang="de">'
    html += getHtmlHeader()
    html += '<body>'
    html += getExecuteTime()
    html += '<div class="container">'
    html += '<div class="row">'
    html += '<div class="col">'
    html += str(erbaHtml)
    html += '</div>'
    html += '<div class="col">'
    html += str(markusHtml)
    html += '</div>'
    html += '</div>'
    html += '<div class="row">'
    html += '<div class="col">'
    html += str(austrHtml)
    html += '</div>'
    html += '<div class="col">'
    html += str(fekiHtml)
    html += '</div>'
    html += '</div>'
    html += '<div class="row">'
    html += '<div class="col">'
    html += str(happyHourHtml)
    html += '</div>'
    html += '</div>'
    html += '</div>'
    html += '</body>'
    html += '</html>'
    return html


def getFoodDiv(html, divClass):
    soup = BeautifulSoup(html, "lxml")
    return soup.find("div", {"class": divClass})


def getHappyHourGuideFood(html):
    soup = BeautifulSoup(html, "lxml")
    return soup.find("div", {"id": "food"})


def getWebPages():
    erbaCafete = requests.get(LINK_ERBA_CAFETE).content
    markusCafete = requests.get(LINK_MARKUS_CAFETE).content
    austrMensa = requests.get(LINK_AUSTR_MENSA).content
    fekiMensa = requests.get(LINK_FEKI_MENSA).content
    happyHourGuide = requests.get(LINK_FEKIDE_GUIDE).content
    return (erbaCafete, markusCafete, austrMensa, fekiMensa, happyHourGuide)


def getSpecificParts():
    erbaCafete, markusCafete, austrMensa, fekiMensa, happyHourGuide = getWebPages()
    erbaCafeteFood = getFoodDiv(erbaCafete, "csc-default")
    markusCafeteFood = getFoodDiv(markusCafete, "csc-default")
    austrMensaFood = getFoodDiv(austrMensa, "day")
    fekiMensaFood = getFoodDiv(fekiMensa, "day")
    happyHourGuideFood = getHappyHourGuideFood(happyHourGuide)
    return (erbaCafeteFood, markusCafeteFood, austrMensaFood, fekiMensaFood, happyHourGuideFood)


def writeHtml(html):
    with open(OUTPUTFILE, "w") as file:
        file.write(html)


def stripCafeteFood(html):
    soup = BeautifulSoup(str(html), "lxml")
    food = soup.find_all("p", {"class": "bodytext"})
    return food[(food.__len__() - 2)]


def htmlErbaCafete(food):
    html = '<h2>Cafeteria Erba-Insel</h2>'
    html += str(food)
    return html


def htmlMarkusCafete(food):
    html = '<h2>Cafeteria Markusplatz</h2>'
    html += str(food)
    return html


def htmlHappyHour(food):
    html = '<h2>Feki.de Happy Hour Guide</h2>'
    html += str(food)
    return html


def getFoodMensa(austrMensaFood, title):
    html = '<div>'
    html += '<h2>' + title + '</h2>'
    soup = BeautifulSoup(str(austrMensaFood), "lxml")
    foodDay = soup.find("div", {"class": "day"}).h5
    html += str(foodDay)
    foods = soup.find_all("article", {"class": "menu"})
    for food in foods:
        soupSingleFood = BeautifulSoup(str(food), "lxml")
        singleFood = soupSingleFood.find("div", {"class": "title"})
        alergenLink = soupSingleFood.find("div", {"class": "additnr"}).a
        html += str(singleFood)
        html += str(alergenLink)
    html += '</div>'
    return html


def main():
    (erbaCafeteFood, markusCafeteFood, austrMensaFood, fekiMensaFood, happyHourGuideFood) = getSpecificParts()
    erbaCafeteFood = stripCafeteFood(erbaCafeteFood)
    erbaCafeteFood = htmlErbaCafete(erbaCafeteFood)
    markusCafeteFood = stripCafeteFood(markusCafeteFood)
    markusCafeteFood = htmlMarkusCafete(markusCafeteFood)
    happyHourGuideFood = htmlHappyHour(happyHourGuideFood)

    austrMensaFood = getFoodMensa(austrMensaFood, "Mensa Austraße")
    fekiMensaFood = getFoodMensa(fekiMensaFood, "Feki Mensa")

    html = getFoodHtml(erbaCafeteFood, markusCafeteFood, austrMensaFood, fekiMensaFood, happyHourGuideFood)
    writeHtml(html)


main()
