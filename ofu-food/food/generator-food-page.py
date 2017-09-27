import jinja2
import json
import datetime
from jinja2 import Environment, FileSystemLoader

# Config global
CSSFILE_WEB = "../css/bootstrap-4.0.0-beta-dist/css/bootstrap.css"
TEMPLATE_PATH = 'food.jinja'

# Config Thinkpad
# JSON_FILES_PATH = "../json/"
# OUTPUT = "../html/food.html"
# JINJA_PATH = 'templates/'


# PI
JSON_FILES_PATH = "/media/data_1/www/pub-html/ofu-food/json/"
OUTPUT = "/media/data_1/www/pub-html/ofu-food/food.html"
JINJA_PATH = '/media/data_1/skripts/ofu-app-webskripts/ofu-food/templates/'


def getJsonFromFile(path):
    with open(path, "r") as file:
        return json.load(file)


def main():
    erbaJson = getJsonFromFile(JSON_FILES_PATH + "erba-cafete.json")
    markusJson = getJsonFromFile(JSON_FILES_PATH + "markus-cafete.json")
    fekiJson = getJsonFromFile(JSON_FILES_PATH + "feki-mensa.json")
    austrJson = getJsonFromFile(JSON_FILES_PATH + "austr-mensa.json")
    fekideJson = getJsonFromFile(JSON_FILES_PATH + "feki-happyhour-guide.json")

    env = Environment(loader=FileSystemLoader(JINJA_PATH))
    template = env.get_template(TEMPLATE_PATH)

    templateVars = {
        "cssfile": CSSFILE_WEB,
        "executiontime": datetime.datetime.today().strftime("%A, %d.%m.%Y"),
        "erbaCafeteTitle": erbaJson['name'],
        "erbaWeekmenu": erbaJson['weekmenu'],
        "markusCafeteTitle": markusJson['name'],
        "markusWeekmenu": markusJson['weekmenu'],
        "austrMensaTitle": austrJson['name'],
        "austrWeekmenu": austrJson['weekmenu'],
        "fekiMensaTitle": fekiJson['name'],
        "fekiWeekmenu": fekiJson['weekmenu'],
        "happyHourDay": fekideJson['day'],
        "happyhours": fekideJson['happyhours'],
    }

    # Template Vars: cssfile, executiontime, erbaCafeteTitle, erbaWeekmenu, markusCafeteTitle, markusWeekmenu, austrMensaTitle, austrWeekmenu, fekiMensaTitle, fekiWeekmenu, happyHourDay, happyhours

    html = template.render(templateVars)

    with open(OUTPUT, "w") as file:
        file.write(html)


main()