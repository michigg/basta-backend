import json
from datetime import datetime
from datetime import timedelta
from pprint import pprint
from django.db.utils import IntegrityError
from apps.events.utils.parser import univis_eventpage_parser
from apps.events.utils.parser import fekide_eventpage_parser

from apps.events.models import Event, Location

UNIVIS_CATEGORY = 'Univis'

# CONFIG
UNIVIS_RPG_GuK = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Geistes-%20und%20Kulturwissenschaften&show=xml"
UNIVIS_RPG_SoWi = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Sozial-%20und%20Wirtschaftswissenschaften&show=xml"
UNIVIS_RPG_HuWi = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Humanwissenschaften&show=xml"
UNIVIS_RPG_WIAI = "http://univis.uni-bamberg.de/prg?search=events&department=Fakult%E4t%20Wirtschaftsinformatik&show=xml"


def writeFekideDataInDB(data):
    for date in data['dates']:
        for event in date['events']:
            try:
                Location.objects.create(name=event['location'])
            except IntegrityError:
                # print("Location %s already exists." % event['location'])
                pass

            try:
                event_obj, new = Event.objects.get_or_create(date=datetime.strptime(date['date'], "%d.%m.%Y"),
                                                             title=event['title'])
                if new:
                    event_obj.category = event['category']
                    event_obj.link = event['link']
                    event_obj.time = datetime.strptime(str(event['time']).split()[1], "%H:%M")
                    event_obj.locations.add(Location.objects.get(name=event['location']))
                    event_obj.save()
                    Event.objects.filter(title="").delete()
                else:
                    print("Event %s already exists. Start Update" % str(event_obj.title))
                    event_obj.category = event['category']
                    event_obj.link = event['link']
                    event_obj.time = datetime.strptime(str(event['time']).split()[1], "%H:%M")
                    event_obj.locations.add(Location.objects.get(name=event['location']))
                    event_obj.save()
            except IntegrityError:
                # ignored
                pass


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
                Location.objects.create(key=room['@key'], name=room['short'])
            except IntegrityError:
                print("Possible Duplicate! Start DB refresh")
                try:
                    Location.objects.get(name=room['short']).key = room['@key']
                except Exception as harderr:
                    print("Failed to refresh object" + harderr.args)
            except Exception as err:
                print(err.args)


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
                    except IntegrityError:
                        # TODO: Update DB Object if duplicate detected
                        print("Found Duplicate!")
                    except Exception as err:
                        print(err.args)
                    Event.objects.filter(title="").delete()


def write_out_db_objects():
    pprint("Event: " + str(Event.objects.count()))
    pprint("Location: " + str(Location.objects.count()))


def main():
    print("Aktueller Stand:")
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

    print("Neuer Stand:")
    write_out_db_objects()


if __name__ == '__main__':
    main()
