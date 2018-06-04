import json
from datetime import datetime
from pprint import pprint
from django.db.utils import IntegrityError
from apps.food.models import SingleFood, Menu, HappyHour, Allergene, HappyHourLocation
from apps.food.utils.parser import mensa_page_parser, fekide_happyhour_page_parser, cafete_page_parser
import logging

logger = logging.getLogger(__name__)

# CONFIG SERVICE LINKS
LINK_FEKI_MENSA = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=3&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=c3fe5ebb35e5fba3794f01878e798b7c"
LINK_AUSTR_MENSA = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=2&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=511e047953ee1370c3b82c11a04624bb"
LINK_ERBA_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-erba-insel.html"
LINK_MARKUS_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-markusplatz.html"
LINK_FEKIDE_GUIDE = "https://www.feki.de/happyhour"

LOCATION_NAMES = ('erba', 'markusplatz', 'feldkirchenstraße', 'austraße')


def getLocation(raw_loc):
    for choice, name in zip(Menu.LOCATION_CHOICES, LOCATION_NAMES):
        if name.upper() in str(raw_loc).upper():
            return choice
    logger.warning("{loc} unknown location".format(loc=raw_loc))
    return None


def writeStudentenwerkDataInDB(data):
    if not data:
        logger.warning('no data')
        return
    logger.info("{location}".format(location=data['name']))
    for menu in data['weekmenu']:
        logger.info("{date}".format(date=menu['date']))
        foodlist = []
        for single_food in menu['menu']:
            logger.info("{}".format(single_food['title']))
            allergens = []
            if 'allergens' in single_food:
                for allergen in single_food['allergens']:
                    allergens.append(Allergene.objects.get_or_create(name=allergen)[0])
            # TODO: Consider keyword arg for price
            try:
                db_single_food, created = SingleFood.objects.get_or_create(name=single_food['title'])
                if 'prices' in single_food:
                    if 'price_student' in single_food['prices']:
                        db_single_food.price_student = single_food['prices']['price_student']
                    else:
                        db_single_food.price_student = "None"
                    if 'price_employee' in single_food['prices']:
                        db_single_food.price_employee = single_food['prices']['price_employee']
                    else:
                        db_single_food.price_employee = "None"
                    if 'price_guest' in single_food['prices']:
                        db_single_food.price_guest = single_food['prices']['price_guest']
                    else:
                        db_single_food.price_guest = "None"
                if allergens:
                    db_single_food.allergens.set(allergens)
                foodlist.append(db_single_food)
                db_single_food.save()
            except IntegrityError as e:
                logger.exception(e)

        try:
            date = datetime.strptime(str(menu['date']), "%d.%m.").replace(year=datetime.today().year)
            menu, _ = Menu.objects.get_or_create(location=getLocation(data['name']), date=date)
            menu.menu.set(foodlist)
            menu.save()
        except IntegrityError as error:
            logger.exception(error)


def writeFekideDataInDB(data):
    for happyhour_data in data['happyhours']:
        time = str(happyhour_data['time']).replace(" ", "").split("-")
        try:
            location, _ = HappyHourLocation.objects.get_or_create(name=happyhour_data['location'])
            happyhour, _ = HappyHour.objects.get_or_create(location=location,
                                                           starttime=datetime.strptime(time[0], "%H:%M").time(),
                                                           endtime=datetime.strptime(time[1], "%H:%M").time())
            happyhour.date = datetime.strptime(data['day'], "%A, %d.%m.%Y")
            happyhour.description = happyhour_data['description']
            happyhour.save()

            logger.info("{date}: Happy Hour: Location: {location}, Description: {description}".format(
                date=happyhour.date,
                location=happyhour.location,
                description=happyhour.description)
            )
        except Exception as e:
            logger.exception(e)


def writeoutDBObjects():
    return "\n\tSingleFood: {single_food}\n\tMenu: {menu}\n\tHappyHour: {happy_hour}".format(
        single_food=SingleFood.objects.count(),
        menu=Menu.objects.count(),
        happy_hour=HappyHour.objects.count()
    )


def delete():
    happy_hours = HappyHour.objects.all()
    logger.info("Deleted following Happy Hours:")
    for happy_hour in happy_hours:
        logger.info("{date}: Happy Hour: Location: {location}, Description: {description}".format(
            date=happy_hour.date,
            location=happy_hour.location,
            description=happy_hour.description)
        )
        happy_hour.delete()


def main():
    logger.info("Aktueller Stand:" + writeoutDBObjects())

    # get food jsons
    logger.info('AUSTRASSE')
    writeStudentenwerkDataInDB(mensa_page_parser.parsePage(LINK_AUSTR_MENSA))
    logger.info('FEKI')
    writeStudentenwerkDataInDB(mensa_page_parser.parsePage(LINK_FEKI_MENSA))
    logger.info('ERBA')
    writeStudentenwerkDataInDB(cafete_page_parser.parse_page(LINK_ERBA_CAFETE))
    logger.info('MARKUSHAUS')
    writeStudentenwerkDataInDB(cafete_page_parser.parse_page(LINK_MARKUS_CAFETE))
    writeFekideDataInDB(fekide_happyhour_page_parser.parse_page(LINK_FEKIDE_GUIDE))

    logger.info("Neuer Stand:" + writeoutDBObjects())


if __name__ == '__main__':
    main()
