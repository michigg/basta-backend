import jinja2
import json
import datetime
from jinja2 import Environment, FileSystemLoader

# Config global
CSSFILE_WEB = "../css/bootstrap-4.0.0-beta-dist/css/bootstrap.css"
TEMPLATE_PATH = 'events.jinja'

# Config Thinkpad
# JSON_FILES_PATH = "../json/"
# OUTPUT = "../html/event.html"
# JINJA_PATH = 'templates/'


# PI
JSON_FILES_PATH = "/media/data_1/www/pub-html/events/json/"
OUTPUT = "/media/data_1/www/pub-html/events/index.html"
JINJA_PATH = '/media/data_1/skripts/ofu-app-webskripts/ofu-food/templates/'


def getJsonFromFile(path):
    with open(path, "r") as file:
        return json.load(file)


def main():
    ofuEventsJson = getJsonFromFile(JSON_FILES_PATH + "events-ofu.json")

    env = Environment(loader=FileSystemLoader(JINJA_PATH))
    template = env.get_template(TEMPLATE_PATH)

    templateVars = {
        "cssfile": CSSFILE_WEB,
        "events_wrapper": ofuEventsJson,
    }

    # Template Vars: cssfile, executiontime, erbaCafeteTitle, erbaWeekmenu, markusCafeteTitle, markusWeekmenu, austrMensaTitle, austrWeekmenu, fekiMensaTitle, fekiWeekmenu, happyHourDay, happyhours

    html = template.render(templateVars)

    with open(OUTPUT, "w") as file:
        file.write(html)


main()
