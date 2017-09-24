import importlib

mensapageparser = importlib.import_module('mensa-page-parser')
cafetepageparser = importlib.import_module('cafete-page-parser')
fekidehappyhourpageparser = importlib.import_module('fekide-happyhour-page-parser')

# JSON_OUTPUT_DIR = "../json/"
# PI
JSON_OUTPUT_DIR = "/media/data_1/www/pub-html/ofu-food/api/json/"

LINK_FEKI_MENSA = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=3&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=c3fe5ebb35e5fba3794f01878e798b7c"
LINK_AUSTR_MENSA = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=2&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=511e047953ee1370c3b82c11a04624bb"
LINK_ERBA_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-erba-insel.html"
LINK_MARKUS_CAFETE = "https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-markusplatz.html"
LINK_FEKIDE_GUIDE = "https://www.feki.de/happyhour"


def writeToFile(jsonfile, filename):
    with open((JSON_OUTPUT_DIR + filename), "w") as file:
        file.write(jsonfile)


def main():
    try:
        fekiMensaJson = mensapageparser.parsePage(LINK_FEKI_MENSA)

    except IndexError:
        print("Error")
        fekiMensaJson = {}

    try:
        austrMensaJson = mensapageparser.parsePage(LINK_AUSTR_MENSA)
    except IndexError:
        print("Error")
        austrMensaJson = {}

    try:
        erbaCafeteJson = cafetepageparser.parsePage(LINK_ERBA_CAFETE)
    except IndexError:
        print("Error")
        erbaCafeteJson = {}

    try:
        markusCafeteJson = cafetepageparser.parsePage(LINK_MARKUS_CAFETE)
    except IndexError:
        print("Error")
        markusCafeteJson = {}

    try:
        fekidehappyhourJson = fekidehappyhourpageparser.parsePage(LINK_FEKIDE_GUIDE)
    except IndexError:
        print("Error")
        fekidehappyhourJson = {}

    writeToFile(fekiMensaJson, "feki-mensa.json")
    writeToFile(austrMensaJson, "austr-mensa.json")
    writeToFile(erbaCafeteJson, "erba-cafete.json")
    writeToFile(markusCafeteJson, "markus-cafete.json")
    writeToFile(fekidehappyhourJson, "feki-happyhour-guide.json")


main()
