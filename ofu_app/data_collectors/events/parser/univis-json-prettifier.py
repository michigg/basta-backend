import json
from pprint import pprint
import datetime


def loadJson(path: str):
    with open(path, 'r') as file:
        return json.load(file)


def deleteNotCalendarElements(data):
    events = []
    for event in data['UnivIS']['Event']:
        if 'calendar' in event:
            if not event['calendar'] == 'nein':
                events.append(event)
    data['UnivIS']['Event'] = events
    # pprint(data['UnivIS']['Event'])


def getRoom(data, id: str):
    for room in data['UnivIS']['Room']:
        if room['@key'] == id:
            return room


def resolveRoomRefs(data):
    for event in data['UnivIS']['Event']:
        if 'rooms' in event:
            rooms = []
            # pprint(event['rooms']['room'])
            if not isinstance(event['rooms']['room'], list):
                single_room = {}
                single_room['room'] = getRoom(data, event['rooms']['room']['UnivISRef']['@key'])['short']
                rooms.append(single_room)

            else:
                for room_item in event['rooms']['room']:
                    single_room = {}
                    single_room['room'] = getRoom(data, room_item['UnivISRef']['@key'])['short']
                    rooms.append(single_room)
            event['rooms'] = rooms
        else:
            event['rooms'] = None


def getContact(data, id: str):
    for contact in data['UnivIS']['Person']:
        if contact['@key'] == id:
            person = {}
            person['atitle'] = None
            if 'atitle' in contact:
                person['atitle'] = contact['atitle']

            person['firstname'] = contact['firstname']
            person['lastname'] = contact['lastname']
            person['email'] = None
            if 'email' in contact['locations']['location']:
                person['email'] = contact['locations']['location']['email']

            person['tel'] = None
            if 'tel' in contact['locations']['location']:
                person['tel'] = contact['locations']['location']['tel']

            person['office'] = None
            if 'office' in contact['locations']['location']:
                person['office'] = contact['locations']['location']['office']

            person['url'] = None
            if 'url' in contact['locations']['location']:
                person['url'] = contact['locations']['location']['url']
    return person


def resolveContactRefs(data):
    for event in data['UnivIS']['Event']:
        key = event['contact']['UnivISRef']['@key']
        event['contact'] = getContact(data, key)


def initalDateBoard(days: int, dateformat: str):
    dates = {}
    dates_arr = []
    now = datetime.datetime.now()
    i = 0
    while i < days:
        date = {}
        day = now + datetime.timedelta(days=i)
        date['date'] = day.strftime(dateformat)
        date['events'] = []
        dates_arr.append(date)
        i += 1

    dates['dates'] = dates_arr
    return dates


def getNewEvent(event):
    new_event = {}
    new_event['title'] = event['title']
    new_event['time'] = event['starttime']
    new_event['endtime'] = event['endtime']
    new_event['category'] = None
    new_event['link'] = None
    locations = []
    if event['rooms']:
        for room in event['rooms']:
            location = {}
            location['location'] = room
            locations.append(location)
    new_event['locations'] = locations
    new_event['description'] = None
    if 'description' in event:
        new_event['description'] = event['description']
    return new_event


def getDateBasedJson(data):
    dateformat = "%d.%m.%Y"
    dates = initalDateBoard(180, dateformat)

    for event in data['UnivIS']['Event']:
        startdate = datetime.datetime.strptime(event['startdate'], "%d.%m.%Y")
        enddate = datetime.datetime.strptime(event['enddate'], "%d.%m.%Y")
        new_event = getNewEvent(event)

        while startdate <= enddate:
            for date in dates['dates']:
                if date['date'] == startdate.strftime(dateformat):
                    date['events'].append(new_event)

            startdate = startdate + datetime.timedelta(days=1)
    return dates


def prettify(json_path: str):
    data = loadJson(json_path)
    deleteNotCalendarElements(data)
    resolveRoomRefs(data)
    resolveContactRefs(data)
    return json.dumps(getDateBasedJson(data))

# prettify("../../../static/html/events/json/events-univis.jason")
