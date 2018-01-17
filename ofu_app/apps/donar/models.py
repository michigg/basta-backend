from django.db import models
from django.utils import timezone

MAX_ROOM_KEY_LENGTH = 256
MAX_ROOM_NAME_LENGTH = 256
MAX_ROOM_ADDRESS_LENGTH = 256
MAX_ROOM_SIZE_LENGTH = 64
MAX_ROOM_DESCRIPTION_LENGTH = 512

MAX_COORDS_NAME_LENGTH = 256
MAX_COORDS_LENGTH = 256

MAX_LECTURE_IDS_LENGTH = 256
MAX_LECTURE_SHORT_LENGTH = 128
MAX_LECTURE_NAME_LENGTH = 256
MAX_LECTURE_TYPE_LENGTH = 64


# Create your models here.
class Room(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=MAX_ROOM_KEY_LENGTH, default="")
    address = models.CharField(max_length=MAX_ROOM_ADDRESS_LENGTH, default="")
    building_key = models.CharField(max_length=MAX_ROOM_KEY_LENGTH, default="")
    floor = models.CharField(max_length=MAX_ROOM_KEY_LENGTH, default="")
    name = models.CharField(max_length=MAX_ROOM_NAME_LENGTH, default="")
    orgname = models.CharField(max_length=MAX_ROOM_KEY_LENGTH, default="")
    short = models.CharField(unique=True, max_length=MAX_ROOM_KEY_LENGTH)
    size = models.CharField(max_length=MAX_ROOM_SIZE_LENGTH, default="")
    description = models.CharField(max_length=MAX_ROOM_DESCRIPTION_LENGTH, default="")

    def __str__(self):
        return "%s - size: %s" % (self.short, str(self.size))


class VGN_Coords(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=MAX_COORDS_NAME_LENGTH, unique=True)
    coords = models.CharField(max_length=MAX_COORDS_LENGTH, unique=True)
    longitude = models.CharField(max_length=MAX_COORDS_LENGTH, unique=True)
    latitude = models.CharField(max_length=MAX_COORDS_LENGTH, unique=True)

    def __str__(self):
        return "%s" % self.name


class Lecture(models.Model):
    id = models.AutoField(primary_key=True)
    univis_ref = models.CharField(max_length=MAX_LECTURE_IDS_LENGTH, unique=True)
    univis_id = models.CharField(max_length=MAX_LECTURE_IDS_LENGTH, unique=True)
    name = models.CharField(max_length=MAX_LECTURE_NAME_LENGTH)
    short = models.CharField(max_length=MAX_LECTURE_SHORT_LENGTH)
    type = models.CharField(max_length=MAX_LECTURE_TYPE_LENGTH)
    lecturer_id = models.CharField(max_length=MAX_LECTURE_IDS_LENGTH)
    term = models.ManyToManyField('Lecture_Terms', blank=False)

    def __str__(self):
        return "%s - Type: %s" % (self.short, str(self.type))


class Lecture_Terms(models.Model):
    id = models.AutoField(primary_key=True)
    starttime = models.TimeField(blank=False)
    room = models.ManyToManyField('Room', blank=True)

    def __str__(self):
        return "%s" % self.starttime.strftime("%Y-%m-%d")
