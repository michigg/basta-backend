import json
from datetime import datetime
from pprint import pprint

import django
import os
from django.db.utils import IntegrityError

os.environ['DJANGO_SETTINGS_MODULE'] = 'ofu_app.settings'
django.setup()
from apps.events.models import Event

# JSON_FILES_PATH_EVENTS = "json_generator/jsons/"
JSON_FILES_PATH_EVENTS = "events/json_generator/jsons/"


def getJsonFromFile(path):
    with open(path, "r") as file:
        return json.load(file)


def writeFekideDataInDB(data):
    for date in data['dates']:
        for event in date['events']:
            try:
                time = datetime.strptime(str(event['time']).split()[1], "%H:%M")
                Event.objects.create(date=datetime.strptime(date['date'], "%d.%m.%Y"), category=event['category'],
                                     link=event['link'], location=event['location'], title=event['title'], time=time)
            except IntegrityError:
                # ignored
                break


def main():
    # get food jsons
    writeFekideDataInDB(getJsonFromFile(JSON_FILES_PATH_EVENTS + "events-fekide.json"))

    pprint("Event: " + str(Event.objects.count()))


main()
