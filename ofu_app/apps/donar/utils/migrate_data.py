import json
from pprint import pprint
from django.db.utils import IntegrityError
from datetime import datetime

from apps.donar.models import Room, Lecture_Terms, Lecture
from apps.donar.utils.parser import univis_rooms_parser
from apps.donar.utils.parser import univis_lectures_parser

# CONFIG Fakultaet
FAKULTAET_GuK = "Fakult%E4t%20Geistes-%20und%20Kulturwissenschaften"
FAKULTAET_SoWi = "Fakult%E4t%20Sozial-%20und%20Wirtschaftswissenschaften"
FAKULTAET_HuWi = "Fakult%E4t%20Humanwissenschaften"
FAKULTAET_WIAI = "Fakult%E4t%20Wirtschaftsinformatik"


# CONFIG ROOMS
def univis_rooms(fakultaet):
    return "http://univis.uni-bamberg.de/prg?search=rooms&department=" + fakultaet + "&show=xml"


# CONFIG LECTURES
def univis_lectures(fakultaet):
    return "http://univis.uni-bamberg.de/prg?search=lectures&department=" + fakultaet + "&show=exml"


def getJsonFromFile(path):
    with open(path, "r") as file:
        return json.load(file)


def writeUnivisRoomDataInDB(data):
    for room in data:
        try:
            key = ""
            address = ""
            building_key = ""
            floor = ""
            name = ""
            orgname = ""
            short = ""
            size = ""
            description = ""
            if '@key' in room:
                key = room['@key']
            if 'address' in room:
                address = room['address']
            if 'buildingkey' in room:
                building_key = room['buildingkey']
            if 'floor' in room:
                floor = room['floor']
            if 'name' in room:
                name = room['name']
            if 'short' in room:
                short = room['short']
            if 'size' in room:
                size = room['size']
            if 'description' in room:
                description = room['description']

            Room.objects.create(key=key, address=address, building_key=building_key, floor=floor, name=name,
                                orgname=orgname, short=short, size=size, description=description)
        except IntegrityError:
            # ignored
            break


def writeUnivisLectureTermsInDB(lecture, lecture_obj):
    if 'terms' in lecture:
        if type(lecture['terms']['term']) == list:
            for term in lecture['terms']['term']:
                try:
                    term_obj = Lecture_Terms.objects.create()
                    starttime = "00:00"
                    if 'starttime' in term:
                        starttime = term['starttime']
                        term_obj.starttime = datetime.strptime(starttime, "%H%H:%M%M")
                    if 'room' in term:
                        room_id = term['room']['UnivISRef']['@key']
                        term_obj.room = Room.objects.get(key=room_id)
                    term_obj.save()
                    lecture_obj.term.add(term_obj)
                except IntegrityError as err:
                    print(err.args)

        else:
            try:
                term_obj = Lecture_Terms.objects.create()
                starttime = "00:00"
                if 'starttime' in lecture['terms']['term']:
                    starttime = lecture['terms']['term']['starttime']
                    term_obj.starttime = datetime.strptime(starttime, "%H%H:%M%M")
                if 'room' in lecture['terms']['term']:
                    room_id = lecture['terms']['term']['room']['UnivISRef']['@key']
                    term_obj.room = Room.objects.get(key=room_id)
                term_obj.save()
                lecture_obj.term.add(term_obj)
            except IntegrityError as err:
                print(err.args)


def writeUnivisLectureDataInDB(data):
    for lecture in data:
        try:
            key = ''
            name = ''
            orgname = ''
            short = ''
            lecture_type = ''
            lecturer_id = ''

            if '@key' in lecture:
                key = lecture['@key']
            if 'name' in lecture:
                # TODO Fix name bug
                name = lecture['name']
            if 'id' in lecture:
                univis_id = lecture['id']
            if 'orgname' in lecture:
                orgname = lecture['orgname']
            if 'short' in lecture:
                short = lecture['short']
            if 'type' in lecture:
                lecture_type = lecture['type']
            if 'dozs' in lecture:
                lecturer_id = dict(lecture['dozs']['doz']['UnivISRef'])['@key']
            lecture_obj = Lecture.objects.create(univis_ref=key, univis_id=univis_id, name=name, short=short,
                                                 type=lecture_type, lecturer_id=lecture_type)
            writeUnivisLectureTermsInDB(lecture, lecture_obj)
            lecture_obj.save()
        except IntegrityError as err:
            print()

    return


def main():
    # get food jsons
    # writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms(FAKULTAET_GuK)))
    # writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms(FAKULTAET_SoWi)))
    # writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms(FAKULTAET_HuWi)))
    # writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms(FAKULTAET_WIAI)))
    pprint("Room: " + str(Room.objects.count()))
    writeUnivisLectureDataInDB(univis_lectures_parser.parsePage(univis_lectures(FAKULTAET_WIAI)))


if __name__ == '__main__':
    main()
