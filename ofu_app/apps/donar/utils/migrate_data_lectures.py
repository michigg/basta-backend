from apps.donar.models import Room, Lecture_Terms, Lecture
from datetime import datetime
import json
from pprint import pprint
from django.db.utils import IntegrityError
from apps.donar.utils.parser import univis_lectures_parser
import logging

logger = logging.getLogger(__name__)

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


def writeUnivisLectureTermsInDB(lecture, lecture_obj):
    if 'terms' in lecture:
        if type(lecture['terms']['term']) == list:
            for term in lecture['terms']['term']:
                try:
                    starttime = "00:00"
                    term_obj = Lecture_Terms.objects.create(starttime=starttime)
                    if 'starttime' in term:
                        starttime = term['starttime']
                        term_obj.starttime = datetime.strptime(starttime, "%H:%M")
                    term_obj.save()
                    if 'room' in term:
                        room_id = term['room']['UnivISRef']['@key']
                        term_obj.room.add(Room.objects.get(key=room_id))
                    lecture_obj.term.add(term_obj)
                except IntegrityError as err:
                    logger.exception(err)

        else:
            try:
                univis_starttime = "00:00"
                term_obj = Lecture_Terms.objects.create(starttime=univis_starttime)
                if 'starttime' in lecture['terms']['term']:
                    univis_starttime = lecture['terms']['term']['starttime']
                    term_obj.starttime = datetime.strptime(univis_starttime, '%H:%M')
                term_obj.save()
                if 'room' in lecture['terms']['term']:
                    room_id = lecture['terms']['term']['room']['UnivISRef']['@key']
                    Room.objects.get(key=room_id)
                    term_obj.room.add(Room.objects.get(key=room_id))
                term_obj.save()
                lecture_obj.term.add(term_obj)
            except IntegrityError as err:
                logger.exception(err)


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
                                                 type=lecture_type, lecturer_id=lecturer_id)
            writeUnivisLectureTermsInDB(lecture, lecture_obj)
            lecture_obj.save()
            logger.info("Lecture: {}".format(lecture_obj.short))
        except IntegrityError as err:
            logger.warning('Lecture already exists')
            # logger.exception(err)

    return


def showStatus(status: str):
    return "\nStatus: {status}\n\tLectures: {lectures}\n\tLecture Terms: {lecture_terms}\n\tRoom: {room}".format(
        status=status,
        lectures=Lecture.objects.count(),
        lecture_terms=Lecture_Terms.objects.count(),
        room=Room.objects.count()
    )


def delete():
    lectures = Lecture.objects.all()
    logger.info("Deleted following Lectures:")
    for lecture in lectures:
        logger.info("Lecture: {name}".format(
            name=lecture.name)
        )
        lecture.delete()


def main():
    # get food jsons
    logger.info(showStatus("Start SoWi:"))
    writeUnivisLectureDataInDB(univis_lectures_parser.parsePage(univis_lectures(FAKULTAET_SoWi)))
    # pprint("----------------------------------------------------------------------------------------")

    logger.info(showStatus("Start GuK:"))
    writeUnivisLectureDataInDB(univis_lectures_parser.parsePage(univis_lectures(FAKULTAET_GuK)))
    # pprint("----------------------------------------------------------------------------------------")

    logger.info(showStatus("Start HuWi:"))
    writeUnivisLectureDataInDB(univis_lectures_parser.parsePage(univis_lectures(FAKULTAET_HuWi)))
    # pprint("----------------------------------------------------------------------------------------")

    logger.info(showStatus("Start WIAI:"))
    writeUnivisLectureDataInDB(univis_lectures_parser.parsePage(univis_lectures(FAKULTAET_WIAI)))
    # pprint("----------------------------------------------------------------------------------------")

    logger.info(showStatus("Finished:"))


if __name__ == '__main__':
    main()
