import importlib

UNIVIS_RPG_URL = "http://univis.uni-bamberg.de/prg?search=events&show=xml"
ofu_event_parser = importlib.import_module('ofu-eventpage-parser')
# fekide_event_parser = importlib.import_module('fekide-eventpage-parser')

JSON_OUTPUT_DIR = "../../json/"


# PI
# JSON_OUTPUT_DIR = "/media/data_1/www/pub-html/events/json/"


def writeToFile(jsonfile, filename):
    with open((JSON_OUTPUT_DIR + filename), "w") as file:
        file.write(jsonfile)


def main():
    try:
        ofuEventsJson = ofu_event_parser.parsePage(UNIVIS_RPG_URL)
    except IndexError:
        print("Error")
        ofuEventsJson = {}

    writeToFile(ofuEventsJson, "events-ofu.json")
    # writeToFile(fekidehappyhourJson, "feki-happyhour-guide.json")


main()
