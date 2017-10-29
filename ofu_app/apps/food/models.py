# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

MAX_LENGTH = 60


# Create your models here.
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=MAX_LENGTH)
    menu = models.ManyToManyField("SingleFood")

    class Meta:
        unique_together = ('date', 'location')

    def __str__(self):
        return "Date: %s, Location: %s" % (self.date.strftime("%d.%m.%Y"), self.location)


class SingleFood(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=MAX_LENGTH)
    price_student = models.CharField(max_length=10, blank=True, null=True)
    price_employee = models.CharField(max_length=10, blank=True, null=True)
    price_guest = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to='food/%Y/%m/', blank=True)
    rating = models.FloatField(default=0)
    allergens = models.ManyToManyField("Allergene", blank=True)

    def __str__(self):
        return "%s - Rating: %f - Student Price: %s" % (self.name, self.rating, self.price_student)


class Allergene(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=MAX_LENGTH)

    def __str__(self):
        return self.name


class HappyHour(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    starttime = models.TimeField(default=timezone.now)
    endtime = models.TimeField(default=timezone.now)
    location = models.CharField(max_length=MAX_LENGTH)
    description = models.CharField(max_length=MAX_LENGTH)

    class Meta:
        unique_together = ('date', 'location', 'starttime', 'endtime')

    def __str__(self):
        return "Date: %s, Location: %s" % (self.date.strftime("%Y.%m.%d"), self.location)


class UserRating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    food = models.ForeignKey(SingleFood)
    rating = models.FloatField(default=0)

    def __str__(self):
        return "User: %s - Rating: %s" % (self.user.username, self.rating)
