from django.db import models

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


