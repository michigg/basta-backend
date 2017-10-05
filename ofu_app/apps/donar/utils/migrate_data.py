import json
from pprint import pprint
from django.db.utils import IntegrityError

from apps.donar.models import Room
from apps.donar.utils.parser import univis_rooms_parser

# CONFIG
UNIVIS_RPG_GuK = "http://univis.uni-bamberg.de/prg?search=rooms&department=Fakult%E4t%20Geistes-%20und%20Kulturwissenschaften&show=xml"
UNIVIS_RPG_SoWi = "http://univis.uni-bamberg.de/prg?search=rooms&department=Fakult%E4t%20Sozial-%20und%20Wirtschaftswissenschaften&show=xml"
UNIVIS_RPG_HuWi = "http://univis.uni-bamberg.de/prg?search=rooms&department=Fakult%E4t%20Humanwissenschaften&show=xml"
UNIVIS_RPG_WIAI = "http://univis.uni-bamberg.de/prg?search=rooms&department=Fakult%E4t%20Wirtschaftsinformatik&show=xml"


def getJsonFromFile(path):
    with open(path, "r") as file:
        return json.load(file)


def writeFekideDataInDB(data):
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


def main():
    # get food jsons
    writeFekideDataInDB(univis_rooms_parser.parsePage(UNIVIS_RPG_GuK))
    writeFekideDataInDB(univis_rooms_parser.parsePage(UNIVIS_RPG_SoWi))
    writeFekideDataInDB(univis_rooms_parser.parsePage(UNIVIS_RPG_HuWi))
    writeFekideDataInDB(univis_rooms_parser.parsePage(UNIVIS_RPG_WIAI))
    pprint("Room: " + str(Room.objects.count()))


if __name__ == '__main__':
    main()
