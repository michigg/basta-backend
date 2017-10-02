import json
from datetime import datetime
from pprint import pprint
from django.db.utils import IntegrityError
from apps.food.models import SingleFood, Menu, HappyHour

# JSON_FILES_PATH_FOOD = "json_generator/jsons/"
JSON_FILES_PATH_FOOD = "food/json_generator/jsons/"


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
            menu.save()
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


def main(path=JSON_FILES_PATH_FOOD):
    # get food jsons
    writeStudentenwerkDataInDB(getJsonFromFile(path + "mensa-austr.json"))
    writeStudentenwerkDataInDB(getJsonFromFile(path + "cafete-erba.json"))
    writeStudentenwerkDataInDB(getJsonFromFile(path + "cafete-markus.json"))
    writeStudentenwerkDataInDB(getJsonFromFile(path + "mensa-feki.json"))

    json_food_fekide = getJsonFromFile(path + "happyhourguide-fekide.json")
    writeFekideDataInDB(json_food_fekide)
    pprint("SingleFood: " + str(SingleFood.objects.count()))
    pprint("Menu: " + str(Menu.objects.count()))
    pprint("HappyHour: " + str(HappyHour.objects.count()))


if __name__ == '__main__':
    main()
