from django.db import models
from django.utils import timezone

MAX_LENGTH = 60


# Create your models here.
class Room(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=MAX_LENGTH, default="")
    address = models.CharField(max_length=MAX_LENGTH, default="")
    building_key = models.CharField(max_length=MAX_LENGTH, default="")
    floor = models.CharField(max_length=MAX_LENGTH, default="")
    name = models.CharField(max_length=MAX_LENGTH, default="")
    orgname = models.CharField(max_length=MAX_LENGTH, default="")
    short = models.CharField(unique=True, max_length=MAX_LENGTH)
    size = models.CharField(max_length=MAX_LENGTH, default="")
    description = models.CharField(max_length=200, default="")


class VGN_Coords(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    coords = models.CharField(max_length=MAX_LENGTH, unique=True)
    longitude = models.CharField(max_length=MAX_LENGTH, unique=True)
    latitude = models.CharField(max_length=MAX_LENGTH, unique=True)


class Lecture(models.Model):
    id = models.AutoField(primary_key=True)
    univis_ref = models.CharField(max_length=MAX_LENGTH, unique=True)
    univis_id = models.CharField(max_length=MAX_LENGTH, unique=True)
    name = models.CharField(max_length=MAX_LENGTH)
    short = models.CharField(max_length=MAX_LENGTH)
    type = models.CharField(max_length=MAX_LENGTH)
    lecturer_id = models.CharField(max_length=MAX_LENGTH)
    term = models.ManyToManyField('Lecture_Terms', blank=False)


class Lecture_Terms(models.Model):
    id = models.AutoField(primary_key=True)
    starttime = time = models.TimeField(blank=False, default=timezone.now())
    room = models.ManyToManyField('Room', blank=False, blank=True, null=True)
