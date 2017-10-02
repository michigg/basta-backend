from apps.events.utils.parser import fekide_eventpage_parser, univis_eventpage_parser, univis_json_prettifier

# CONFIG
JSON_OUTPUT_DIR_EVENTS = "./events/json_generator/jsons/"


def writeToFile(jsonfile, root, filename):
    with open((root + filename), "w") as file:
        file.write(jsonfile)


def main(path=JSON_OUTPUT_DIR_EVENTS):
    try:
        json_events_univis = univis_eventpage_parser.parsePage()
    except Exception as err:
        print(err.args)
        json_events_univis = "{}"

    writeToFile(json_events_univis, path, "events-univis.json")

    try:
        json_events_univis_pretty = univis_json_prettifier.prettify(path + "events-univis.json")
    except Exception as err:
        print(err.args)
        json_events_univis_pretty = "{}"

    try:
        json_events_fekide = fekide_eventpage_parser.parsePage()
    except:
        print("Error")
        json_events_fekide = "{}"

    writeToFile(json_events_univis_pretty, path, "events-univis-pretty.json")
    writeToFile(json_events_fekide, path, "events-fekide.json")


if __name__ == '__main__':
    main()
