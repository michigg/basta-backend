import jinja2
import json
import datetime
from jinja2 import Environment, FileSystemLoader
from pprint import pprint

# Config global

TEMPLATE_PATH = 'events.jinja'

# Config Thinkpad
CSSFILE_WEB = "../css/bootstrap-4.0.0-beta-dist/css/bootstrap.css"
JSON_FILES_PATH = "../json/"
OUTPUT = "../html/event.html"
JINJA_PATH = 'templates/'


# PI
# CSSFILE_WEB = "../../css/bootstrap-4.0.0-beta-dist/css/bootstrap.css"
# JSON_FILES_PATH = "/media/data_1/www/pub-html/events/json/"
# OUTPUT = "/media/data_1/www/pub-html/events/index.html"
# JINJA_PATH = '/media/data_1/skripts/ofu-app-webskripts/ofu-food/templates/'


def getJsonFromFile(path):
    with open(path, "r") as file:
        return json.load(file)


def getTemplate():
    env = Environment(loader=FileSystemLoader(JINJA_PATH))
    return env.get_template(TEMPLATE_PATH)


def writeHtml(html):
    with open(OUTPUT, "w") as file:
        file.write(html)


def resolveDates(json):
    for event in json['UnivIS']['Event']:
        start_datetime = datetime.datetime.strptime(event['startdate'], "%Y-%m-%d").strftime("%d.%m.%Y")
        event['startdate'] = start_datetime
        end_datetime = datetime.datetime.strptime(event['enddate'], "%Y-%m-%d").strftime("%d.%m.%Y")
        event['enddate'] = end_datetime


def main():
    ofuEventsJson = getJsonFromFile(JSON_FILES_PATH + "events-ofu.json")
    resolveDates(ofuEventsJson)
    template = getTemplate()

    templateVars = {
        "cssfile": CSSFILE_WEB,
        "events_wrapper": ofuEventsJson,
    }

    writeHtml(template.render(templateVars))


main()
