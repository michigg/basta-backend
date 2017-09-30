from __future__ import unicode_literals
from django.utils import timezone
from django.db import models

MAX_LENGTH = 60


# Create your models here.
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=MAX_LENGTH)
    category = models.CharField(max_length=MAX_LENGTH)
    link = models.CharField(max_length=MAX_LENGTH)
    location = models.CharField(max_length=MAX_LENGTH)
    time = models.TimeField(default=timezone.now)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('date', 'location')
