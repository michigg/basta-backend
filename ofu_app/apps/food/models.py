# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models

MAX_LENGTH = 60


# Create your models here.
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=MAX_LENGTH)
    menu = models.ManyToManyField("SingleFood")

    class Meta:
        unique_together = ('date', 'location')

    # def __str__(self):
    #    return self.date.strftime("%d.%m.%Y")


class SingleFood(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=MAX_LENGTH)

    # def __str__(self):
    #    return self.name


class HappyHour(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    starttime = models.DateField(default=timezone.now)
    endtime = models.DateField(default=timezone.now)
    location = models.CharField(max_length=MAX_LENGTH)
    description = models.CharField(max_length=MAX_LENGTH)

    class Meta:
        unique_together = ('date', 'location')

    # def __str__(self):
    #    return "Date: %s, Location: %s" % (self.date.strftime("%Y.%m.%d"), self.location)
