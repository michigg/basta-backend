import json
from datetime import datetime
from pprint import pprint
from django.db.utils import IntegrityError
from apps.food.models import SingleFood, Menu, HappyHour, Allergene
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
    pprint(data)
    for menu in data['weekmenu']:
        pprint(menu)
        foodlist = []
        for single_food in menu['menu']:
            pprint(single_food)
            if 'allergens' in single_food:
                allergens = []
                for allergen in single_food['allergens']:
                    try:
                        allergens.append(Allergene.objects.create(name=allergen))
                    except IntegrityError:
                        allergens.append(Allergene.objects.get(name=allergen))
            try:
                if 'prices' in single_food:
                    if 'price_student' in single_food['prices']:
                        price_student = single_food['prices']['price_student']
                    else:
                        price_student = "None"
                    if 'price_employee' in single_food['prices']:
                        price_employee = single_food['prices']['price_employee']
                    else:
                        price_employee = "None"
                    if 'price_guest' in single_food['prices']:
                        price_guest = single_food['prices']['price_guest']
                    else:
                        price_guest = "None"
                    db_single_food = SingleFood.objects.create(name=single_food['title'],
                                                               price_student=price_student,
                                                               price_employee=price_employee,
                                                               price_guest=price_guest)
                else:
                    db_single_food = SingleFood.objects.create(name=single_food['title'])
                if 'allergens' in locals():
                    db_single_food.allergens = allergens
                foodlist.append(db_single_food)
            except IntegrityError:
                db_single_food = SingleFood.objects.get(name=single_food['title'])
                if 'prices' in single_food:
                    if 'price_student' in single_food['prices']:
                        db_single_food.price_student = single_food['prices']['price_student']
                    if 'price_employee' in single_food['prices']:
                        db_single_food.price_employee = single_food['prices']['price_employee']
                    if 'price_guest' in single_food['prices']:
                        db_single_food.price_guest = single_food['prices']['price_guest']
                if 'allergens' in locals():
                    db_single_food.allergens = allergens
                foodlist.append(db_single_food)
        try:
            date = datetime.strptime(str(menu['date']), "%d.%m.").replace(year=datetime.today().year)
            menu = Menu.objects.create(location=data['name'], date=date)
            menu.menu.set(foodlist)
            menu.save()
        except IntegrityError as error:
            # ignored
            pass


def writeFekideDataInDB(data):
    for happyhour_data in data['happyhours']:
        time = str(happyhour_data['time']).replace(" ", "").split("-")
        happyhour, new = HappyHour.objects.get_or_create(date=datetime.strptime(data['day'], "%A, %d.%m.%Y"),
                                                         location=happyhour_data['location'],
                                                         description=happyhour_data['description'],
                                                         starttime=datetime.strptime(time[0], "%H:%M").time(),
                                                         endtime=datetime.strptime(time[1], "%H:%M").time())
        if not new:
            happyhour.date = datetime.strptime(data['day'], "%A, %d.%m.%Y")
            happyhour.location = happyhour_data['location']
            happyhour.description = happyhour_data['description']
            happyhour.starttime = datetime.strptime(time[0], "%H:%M").time()
            happyhour.endtime = datetime.strptime(time[1], "%H:%M").time()
            happyhour.save()

        print("%s: Happy Hour: Location: %s, Description: %s" % (
            str(happyhour.date.date()), str(happyhour.location), str(happyhour.description)))


def writeoutDBObjects():
    pprint("SingleFood: " + str(SingleFood.objects.count()))
    pprint("Menu: " + str(Menu.objects.count()))
    pprint("HappyHour: " + str(HappyHour.objects.count()))


def delete():
    happy_hours = HappyHour.objects.all()
    print("Deleted following Happy Hours:")
    for happy_hour in happy_hours:
        print("%s: Happy Hour: Location: %s, Description: %s" % (
            str(happy_hour.date), str(happy_hour.location), str(happy_hour.description)))
        happy_hour.delete()


def main():
    print("Aktueller Stand:")
    writeoutDBObjects()
    # get food jsons
    writeStudentenwerkDataInDB(mensa_page_parser.parsePage(LINK_AUSTR_MENSA))
    writeStudentenwerkDataInDB(mensa_page_parser.parsePage(LINK_FEKI_MENSA))
    writeStudentenwerkDataInDB(cafete_page_parser.parsePage(LINK_ERBA_CAFETE))
    writeStudentenwerkDataInDB(cafete_page_parser.parsePage(LINK_MARKUS_CAFETE))
    writeFekideDataInDB(fekide_happyhour_page_parser.parsePage(LINK_FEKIDE_GUIDE))

    print("Neuer Stand:")
    writeoutDBObjects()


if __name__ == '__main__':
    main()
