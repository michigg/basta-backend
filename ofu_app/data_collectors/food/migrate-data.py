import json
from pprint import pprint
import django, os
from datetime import datetime
from django.db.utils import IntegrityError

os.environ['DJANGO_SETTINGS_MODULE'] = 'ofu_app.settings'
django.setup()
from food.models import SingleFood, Menu, HappyHour

JSON_FILES_PATH_FOOD = "json_generator/jsons/"


def getJsonFromFile(path):
    with open(path, "r") as file:
        return json.load(file)


def writeStudentenwerkDataInDB(data):
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
        except IntegrityError:
            # ignored
            break


def writeFekideDataInDB(data):
    for happyhour_data in data['happyhours']:
        time = str(happyhour_data['time']).replace(" ", "").split("-")
        try:
            HappyHour.objects.create(date=datetime.strptime(data['day'], "%A, %d.%m.%Y"),
                                     location=happyhour_data['location'], description=happyhour_data['description'],
                                     starttime=datetime.strptime(time[0], "%H:%M"),
                                     endtime=datetime.strptime(time[1], "%H:%M"))
        except IntegrityError:
            # ignored
            break


def main():
    # get food jsons
    writeStudentenwerkDataInDB(getJsonFromFile(JSON_FILES_PATH_FOOD + "mensa-austr.json"))
    writeStudentenwerkDataInDB(getJsonFromFile(JSON_FILES_PATH_FOOD + "cafete-erba.json"))
    writeStudentenwerkDataInDB(getJsonFromFile(JSON_FILES_PATH_FOOD + "cafete-markus.json"))
    writeStudentenwerkDataInDB(getJsonFromFile(JSON_FILES_PATH_FOOD + "mensa-feki.json"))

    json_food_fekide = getJsonFromFile(JSON_FILES_PATH_FOOD + "happyhourguide-fekide.json")
    writeFekideDataInDB(json_food_fekide)
    pprint("SingleFood: " + str(SingleFood.objects.count()))
    pprint("Menu: " + str(Menu.objects.count()))
    pprint("HappyHour: " + str(HappyHour.objects.count()))


main()
