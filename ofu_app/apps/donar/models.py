from django.db import models

MAX_LENGTH = 60


# Create your models here.
class Room(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=MAX_LENGTH)
    address = models.CharField(max_length=MAX_LENGTH)
    building_key = models.CharField(max_length=MAX_LENGTH)
    floor = models.CharField(max_length=MAX_LENGTH)
    name = models.CharField(max_length=MAX_LENGTH)
    orgname = models.CharField(max_length=MAX_LENGTH)
    short = models.CharField(max_length=MAX_LENGTH)
