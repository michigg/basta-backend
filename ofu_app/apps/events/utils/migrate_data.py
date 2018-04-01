import json
from datetime import datetime
from datetime import timedelta
from pprint import pprint
from django.db.utils import IntegrityError
from apps.events.utils.parser import univis_eventpage_parser
from apps.events.utils.parser import fekide_eventpage_parser

from apps.events.models import Event, Location
import logging

logger = logging.getLogger(__name__)

UNIVIS_CATEGORY = 'Univis'

# CONFIG
UNIVIS_RPG_GuK = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Geistes-%20und%20Kulturwissenschaften&show=xml"
UNIVIS_RPG_SoWi = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Sozial-%20und%20Wirtschaftswissenschaften&show=xml"
UNIVIS_RPG_HuWi = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Humanwissenschaften&show=xml"
UNIVIS_RPG_WIAI = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Wirtschaftsinformatik&show=xml"


def writeFekideDataInDB(data):
    for date in data['dates']:
        for event in date['events']:
            location, _ = Location.objects.get_or_create(name=event['location'])
            location.save()

            event_obj, _ = Event.objects.get_or_create(date=datetime.strptime(date['date'], "%d.%m.%Y"),
                                                       title=event['title'])
            event_obj.category = event['category']
            event_obj.link = event['link']
            event_obj.time = datetime.strptime(str(event['time']).split()[1], "%H:%M")
            event_obj.locations.add(Location.objects.get(name=event['location']))
            event_obj.save()
            logger.info('CREATED - Event: {}'.format(event_obj.title))


def deleteUnivisObjects():
    Event.objects.filter(category=UNIVIS_CATEGORY).delete()
    Location.objects.all().delete()


def writeUnivisDataInDB(events, rooms, persons):
    writeUnivisLocationsInDB(rooms)
    writeUnivisEventsInDB(events)


def writeUnivisLocationsInDB(rooms):
    for room in rooms:
        if '@key' in room and 'short' in room:
            try:
                location, _ = Location.objects.get_or_create(key=room['@key'], name=room['short'])
                location.key = room['@key']
                location.name = room['short']
                location.save()
                logger.info('CREATE - Location: {}'.format(location.name))
            except Exception as err:
                logger.critical(err.args)


def getLocationIDs(event):
    rooms = []
    if not isinstance(event['rooms']['room'], list):
        rooms.append(event['rooms']['room']['UnivISRef']['@key'])
    else:
        for room_item in event['rooms']['room']:
            rooms.append(room_item['UnivISRef']['@key'])
    return rooms


def writeUnivisEventsInDB(events: list):
    for event in events:
        if 'calendar' in event and not event['calendar'] == 'nein' and 'internal' in event and event[
            'internal'] == 'nein' and 'startdate' in event and 'enddate' in event:
            startdate = datetime.strptime(event['startdate'], "%Y-%m-%d")
            enddate = datetime.strptime(event['enddate'], "%Y-%m-%d")
            if (startdate + timedelta(1)) >= enddate:

                if 'title' in event and 'rooms' in event and 'starttime' in event:
                    # TODO: Add Description in
                    # TODO: Is there a better way to add Objects in DB?
                    event_obj = Event()
                    event_obj.save()
                    event_obj.title = event['title']
                    locations = getLocationIDs(event)
                    for location in locations:
                        event_obj.locations.add(Location.objects.get(key=location))
                    event_obj.time = event['starttime']
                    event_obj.date = event['startdate']
                    # TODO: Better Category handling
                    event_obj.category = UNIVIS_CATEGORY
                    if 'presenter' in event:
                        event_obj.presenter = event['presenter']
                    if 'orgname' in event:
                        event_obj.orgname = event['orgname']
                    try:
                        event_obj.save()
                        logger.info(event_obj.title)
                    except IntegrityError:
                        # TODO: Update DB Object if duplicate detected
                        logger.info("Found Duplicate!")
                    except Exception as err:
                        logger.exception(err.args)
                    Event.objects.filter(title="").delete()


def write_out_db_objects():
    return "\n\tEvent: {event}\n\tLocation: {location}".format(
        event=Event.objects.count(),
        location=Location.objects.count(),
    )


def main():
    logger.info("Aktueller Stand:")
    write_out_db_objects()

    # deleteUnivisObjects()
    # events, rooms, persons = univis_eventpage_parser.parsePage(UNIVIS_RPG_HuWi)
    # writeUnivisRoomDataInDB(events, rooms, persons)
    # events, rooms, persons = univis_eventpage_parser.parsePage(UNIVIS_RPG_SoWi)
    # writeUnivisRoomDataInDB(events, rooms, persons)
    # events, rooms, persons = univis_eventpage_parser.parsePage(UNIVIS_RPG_GuK)
    # writeUnivisRoomDataInDB(events, rooms, persons)
    # events, rooms, persons = univis_eventpage_parser.parsePage(UNIVIS_RPG_WIAI)
    # writeUnivisRoomDataInDB(events, rooms, persons)

    writeFekideDataInDB(fekide_eventpage_parser.parsePage())

    logger.info("Neuer Stand:")
    write_out_db_objects()


if __name__ == '__main__':
    main()
