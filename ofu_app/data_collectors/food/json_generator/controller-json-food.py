import importlib

# OWN MODULS
parser_food_mensa = importlib.import_module('data_collectors.food.parser.mensa-page-parser')
parser_food_cafete = importlib.import_module('data_collectors.food.parser.cafete-page-parser')
parser_food_fekidehappyhour = importlib.import_module('data_collectors.food.parser.fekide-happyhour-page-parser')

# CONFIG
JSON_OUTPUT_DIR_FOOD = "./jsons/"

# CONFIG SERVICE LINKS
LINK_FEKI_MENSA = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=3&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=c3fe5ebb35e5fba3794f01878e798b7c"
LINK_AUSTR_MENSA = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=2&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=511e047953ee1370c3b82c11a04624bb"
LINK_ERBA_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-erba-insel.html"
LINK_MARKUS_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-markusplatz.html"
LINK_FEKIDE_GUIDE = "https://www.feki.de/happyhour"


def writeToFile(jsonfile, root, filename):
    with open((root + filename), "w") as file:
        file.write(jsonfile)


def main():
    try:
        json_food_mensa_feki = parser_food_mensa.parsePage(LINK_FEKI_MENSA)

    except IndexError:
        print("Error")
        json_food_mensa_feki = {}

    try:
        json_food_mensa_austr = parser_food_mensa.parsePage(LINK_AUSTR_MENSA)
    except IndexError:
        print("Error")
        json_food_mensa_austr = {}

    try:
        json_food_cafete_erba = parser_food_cafete.parsePage(LINK_ERBA_CAFETE)
    except IndexError:
        print("Error")
        json_food_cafete_erba = {}

    try:
        json_food_cafete_markus = parser_food_cafete.parsePage(LINK_MARKUS_CAFETE)
    except IndexError:
        print("Error")
        json_food_cafete_markus = {}

    try:
        json_food_fekidehappyhours = parser_food_fekidehappyhour.parsePage(LINK_FEKIDE_GUIDE)
    except IndexError:
        print("Error")
        json_food_fekidehappyhours = {}

    # WRITE JSONS
    writeToFile(json_food_mensa_feki, JSON_OUTPUT_DIR_FOOD, "mensa-feki.json")
    writeToFile(json_food_mensa_austr, JSON_OUTPUT_DIR_FOOD, "mensa-austr.json")
    writeToFile(json_food_cafete_erba, JSON_OUTPUT_DIR_FOOD, "cafete-erba.json")
    writeToFile(json_food_cafete_markus, JSON_OUTPUT_DIR_FOOD, "cafete-markus.json")
    writeToFile(json_food_fekidehappyhours, JSON_OUTPUT_DIR_FOOD, "happyhourguide-fekide.json")


main()
