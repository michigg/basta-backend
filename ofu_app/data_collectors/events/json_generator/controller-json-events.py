import importlib

# OWN MODULS
parser_event_univis = importlib.import_module('data_collectors.events.parser.univis-eventpage-parser')
parser_event_univis_pretty = importlib.import_module('data_collectors.events.parser.univis-json-prettifier')
parser_event_fekide = importlib.import_module('data_collectors.events.parser.fekide-eventpage-parser')

# CONFIG
JSON_OUTPUT_DIR_EVENTS = "./events/json_generator/jsons/"


def writeToFile(jsonfile, root, filename):
    with open((root + filename), "w") as file:
        file.write(jsonfile)


def main():
    try:
        json_events_univis = parser_event_univis.parsePage()
    except:
        print("Error")
        json_events_univis = "{}"

    writeToFile(json_events_univis, JSON_OUTPUT_DIR_EVENTS, "events-univis.json")

    try:
        json_events_univis_pretty = parser_event_univis_pretty.prettify(JSON_OUTPUT_DIR_EVENTS + "events-univis.json")
    except:
        print("Error")
        json_events_univis_pretty = "{}"

    try:
        json_events_fekide = parser_event_fekide.parsePage()
    except:
        print("Error")
        json_events_fekide = "{}"

    writeToFile(json_events_univis_pretty, JSON_OUTPUT_DIR_EVENTS, "events-univis-pretty.json")
    writeToFile(json_events_fekide, JSON_OUTPUT_DIR_EVENTS, "events-fekide.json")


main()
