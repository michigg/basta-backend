import json
from datetime import datetime
from pprint import pprint
from django.db.utils import IntegrityError
from apps.food.models import SingleFood, Menu, HappyHour
from apps.food.utils.parser import mensa_page_parser, fekide_happyhour_page_parser, cafete_page_parser

# CONFIG SERVICE LINKS
LINK_FEKI_MENSA = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=3&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=c3fe5ebb35e5fba3794f01878e798b7c"
LINK_AUSTR_MENSA = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=2&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=511e047953ee1370c3b82c11a04624bb"
LINK_ERBA_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-erba-insel.html"
LINK_MARKUS_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-markusplatz.html"
LINK_FEKIDE_GUIDE = "https://www.feki.de/happyhour"


def getJsonFromFile(path):
    with open(path, "r") as file:
        return json.load(file)


def writeStudentenwerkDataInDB(data):
    data = json.loads(data)
    for menu in data['weekmenu']:
        foodlist = []
        for single_food in menu['menu']:
            try:
                foodlist.append(SingleFood.objects.create(name=single_food))
            except IntegrityError:
                foodlist.append(SingleFood.objects.get(name=single_food))
        try:
            date = datetime.strptime(str(menu['date']), "%d.%m.").replace(year=datetime.today().year)
            menu = Menu.objects.create(location=data['name'],
                                       date=date)
            menu.menu = foodlist
            menu.save()
        except IntegrityError:
            # ignored
            break


def writeFekideDataInDB(data):
    for happyhour_data in data['happyhours']:
        time = str(happyhour_data['time']).replace(" ", "").split("-")
        happyhour, new = HappyHour.objects.get_or_create(date=datetime.strptime(data['day'], "%A, %d.%m.%Y"),
                                                         location=happyhour_data['location'],
                                                         description=happyhour_data['description'],
                                                         starttime=datetime.strptime(time[0], "%H:%M"),
                                                         endtime=datetime.strptime(time[1], "%H:%M"))
        if not new:
            happyhour.date = datetime.strptime(data['day'], "%A, %d.%m.%Y")
            happyhour.location = happyhour_data['location']
            happyhour.description = happyhour_data['description']
            happyhour.starttime = datetime.strptime(time[0], "%H:%M")
            happyhour.endtime = datetime.strptime(time[1], "%H:%M")


def main():
    # get food jsons
    writeStudentenwerkDataInDB(mensa_page_parser.parsePage(LINK_AUSTR_MENSA))
    writeStudentenwerkDataInDB(mensa_page_parser.parsePage(LINK_FEKI_MENSA))
    writeStudentenwerkDataInDB(cafete_page_parser.parsePage(LINK_ERBA_CAFETE))
    writeStudentenwerkDataInDB(cafete_page_parser.parsePage(LINK_MARKUS_CAFETE))
    writeFekideDataInDB(fekide_happyhour_page_parser.parsePage(LINK_FEKIDE_GUIDE))

    pprint("SingleFood: " + str(SingleFood.objects.count()))
    pprint("Menu: " + str(Menu.objects.count()))
    pprint("HappyHour: " + str(HappyHour.objects.count()))


if __name__ == '__main__':
    main()
