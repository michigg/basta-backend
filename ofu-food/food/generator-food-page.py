import jinja2
import json
import datetime
from jinja2 import Environment, FileSystemLoader

# Config global
CSSFILE_WEB = "../css/bootstrap-4.0.0-beta-dist/css/bootstrap.css"

# Config Thinkpad
JSON_FILES_PATH = "../json/"
OUTPUT = "../html/food.html"
JINJA_PATH = 'templates/'
TEMPLATE_PATH = 'food.jinja'


# PI
# JSON_FILES_PATH = "/media/data_1/www/pub-html/ofu-food/json/"
# OUTPUT = "/media/data_1/www/pub-html/ofu-food/food.html"
# CSSFILE_SRC = "../bootstrap-4.0.0-beta-dist"
# CSSFILE_DEST = "/media/data_1/www/css"


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
    # templateLoader = jinja2.FileSystemLoader(searchpath="./")
    # templateEnv = jinja2.Environment(loader=templateLoader)

    # TEMPLATE_FILE = "templates/food.jinja"
    # template = templateEnv.get_template(TEMPLATE_FILE)

    # Template Vars: cssfile, executiontime, erbaCafeteTitle, erbaWeekmenu, markusCafeteTitle, markusWeekmenu, austrMensaTitle, austrWeekmenu, fekiMensaTitle, fekiWeekmenu, happyHourDay, happyhours

    # html = template.render(templateVars)

    html = template.render(templateVars)

    with open(OUTPUT, "w") as file:
        file.write(html)


main()
