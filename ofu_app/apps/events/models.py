from __future__ import unicode_literals
from django.utils import timezone
from django.db import models

MAX_LENGTH = 60


# Create your models here.
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(blank=False, max_length=MAX_LENGTH)
    category = models.CharField(blank=False, max_length=MAX_LENGTH)
    link = models.CharField(blank=True, max_length=MAX_LENGTH)
    locations = models.ManyToManyField('Location', blank=False)
    date = models.DateField(blank=False, default=timezone.now)
    time = models.TimeField(blank=False, default=timezone.now)
    presenter = models.CharField(blank=True, max_length=MAX_LENGTH)
    orgname = models.CharField(blank=True, max_length=MAX_LENGTH)

    def __str__(self):
        return "Date: %s, Titel: %s" % (self.date.strftime("%Y.%m.%d"), self.title)

    class Meta:
        unique_together = ('date', 'time', 'title')


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(blank=True, max_length=MAX_LENGTH)
    name = models.CharField(blank=False, unique=True, max_length=MAX_LENGTH)

    def __str__(self):
        return str(self.name)
