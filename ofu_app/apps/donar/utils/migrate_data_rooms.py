import json
from pprint import pprint
from django.db.utils import IntegrityError

from apps.donar.models import Room, Lecture_Terms, Lecture
from apps.donar.utils.parser import univis_rooms_parser
from apps.donar.utils.parser import univis_lectures_parser

# CONFIG Fakultaet
FAKULTAET_GuK = "Fakult%E4t%20Geistes-%20und%20Kulturwissenschaften"
FAKULTAET_SoWi = "Fakult%E4t%20Sozial-%20und%20Wirtschaftswissenschaften"
FAKULTAET_HuWi = "Fakult%E4t%20Humanwissenschaften"
FAKULTAET_WIAI = "Fakult%E4t%20Wirtschaftsinformatik"

# CONFIG Locations
RZ = "http://univis.uni-bamberg.de/prg?search=rooms&name=rz&show=xml"
WEBEREI = "http://univis.uni-bamberg.de/prg?search=rooms&name=we&show=xml"
FEKI = "http://univis.uni-bamberg.de/prg?search=rooms&name=f&show=xml"
MARKUSHAUS = "http://univis.uni-bamberg.de/prg?search=rooms&name=m&show=xml"
UNIVERSITAET = "http://univis.uni-bamberg.de/prg?search=rooms&name=u&show=xml"
KAPUZINERSTR = "http://univis.uni-bamberg.de/prg?search=rooms&name=k&show=xml"
ZWINGER = "http://univis.uni-bamberg.de/prg?search=rooms&name=z&show=xml"
AULA = "http://univis.uni-bamberg.de/prg?search=rooms&name=a&show=xml"
ZWINGER = "http://univis.uni-bamberg.de/prg?search=rooms&name=k&show=xml"
ZWINGER = "http://univis.uni-bamberg.de/prg?search=rooms&name=k&show=xml"


# CONFIG ROOMS
def univis_rooms(fakultaet):
    return "http://univis.uni-bamberg.de/prg?search=rooms&department=" + fakultaet + "&show=xml"


# CONFIG LECTURES
def univis_lectures(fakultaet):
    return "http://univis.uni-bamberg.de/prg?search=lectures&department=" + fakultaet + "&show=exml"


def univis_rooms_loc(kuerzel):
    return "http://univis.uni-bamberg.de/prg?search=rooms&name=" + kuerzel + "&show=xml"


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
        except IntegrityError as err:
            pprint(err.args)


def main():
    # get food jsons
    pprint("Begin: Room: " + str(Room.objects.count()))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms(FAKULTAET_GuK)))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms(FAKULTAET_SoWi)))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms(FAKULTAET_HuWi)))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms(FAKULTAET_WIAI)))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("k")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("z")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("u")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("w")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("f")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("r")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("h")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("l")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("m")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("o")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("p")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("v")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("w")))
    writeUnivisRoomDataInDB(univis_rooms_parser.parsePage(univis_rooms_loc("d")))

    pprint("Now: Room: " + str(Room.objects.count()))


if __name__ == '__main__':
    main()
