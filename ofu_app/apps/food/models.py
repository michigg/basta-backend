# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from io import BytesIO
import uuid
from _datetime import datetime

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

MAX_LENGTH = 256
MAX_FOOD_NAME = 256
MAX_FOOD_LOCATION_LENGTH = 256
MAX_FOOD_PRICE_LENGTH = 10
MAX_FOOD_ALLERGENNAME_LENGTH = 256
MAX_HAPPY_HOUR_LOCATION_LENGTH = 256
MAX_HAPPY_HOUR_DESCRIPTION_LENGTH = 1024
MAX_FOOD_COMMENT_TITLE_LENGTH = 128
MAX_FOOD_COMMENT_LENGTH = 2048


def image_path(instance, filename):
    extension = filename.split('.')[-1]
    date = datetime.now().strftime('%Y/%m/%W')
    return 'food/originals/{}/{}.{}'.format(date, uuid.uuid4(), extension)


def thumb_path(instance, filename):
    extension = filename.split('.')[-1]
    date = datetime.now().strftime('%Y/%m/%W')
    return 'food/thumbs/{}/{}.{}'.format(date, uuid.uuid4(), 'jpg')


# Create your models here.
class Menu(models.Model):
    ERBA = 'ERBA'
    MARKUSPLATZ = 'MARKUSPLATZ'
    FEKI = 'FEKI'
    AUSTRASSE = 'AUSTRASSE'

    LOCATION_CHOICES = (
        (ERBA, 'Erba'), (MARKUSPLATZ, 'Markusplatz'), (FEKI, 'Feldkirchenstrasse'), (AUSTRASSE, 'Austrasse'))

    # Api location data
    API_LOCATIONS = [{'id': FEKI, 'name': 'Feldkirchenstrasse', 'short': 'Feki'},
                     {'id': AUSTRASSE, 'name': 'Austrasse', 'short': 'Austrasse'},
                     {'id': ERBA, 'name': 'Erba', 'short': 'Erba'},
                     {'id': MARKUSPLATZ, 'name': 'Markusplatz', 'short': 'Markusplatz'}, ]

    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=MAX_FOOD_LOCATION_LENGTH, choices=LOCATION_CHOICES)
    menu = models.ManyToManyField("SingleFood", related_name="foods")

    class Meta:
        unique_together = ('date', 'location')

    def __str__(self):
        return "Date: %s, Location: %s" % (self.date.strftime("%d.%m.%Y"), self.location)


class SingleFood(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=MAX_FOOD_NAME)
    price_student = models.CharField(max_length=MAX_FOOD_PRICE_LENGTH, blank=True, null=True)
    price_employee = models.CharField(max_length=MAX_FOOD_PRICE_LENGTH, blank=True, null=True)
    price_guest = models.CharField(max_length=MAX_FOOD_PRICE_LENGTH, blank=True, null=True)
    image = models.ForeignKey('FoodImage', on_delete=models.SET_NULL, blank=True, null=True)
    rating = models.FloatField(default=0)
    allergens = models.ManyToManyField("Allergene", blank=True)
    comments = models.ManyToManyField('UserFoodComment', blank=True)

    def __str__(self):
        return "%s - Rating: %f - Student Price: %s" % (self.name, self.rating, self.price_student)


class Allergene(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=MAX_FOOD_ALLERGENNAME_LENGTH)

    def __str__(self):
        return self.name


class HappyHour(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    starttime = models.TimeField(default=timezone.now)
    endtime = models.TimeField(default=timezone.now)
    location = models.ForeignKey('HappyHourLocation', on_delete=models.PROTECT)
    description = models.CharField(max_length=MAX_HAPPY_HOUR_DESCRIPTION_LENGTH)

    class Meta:
        unique_together = ('location', 'starttime', 'endtime')

    def __str__(self):
        return "Date: %s, Location: %s" % (self.date.strftime("%Y.%m.%d"), self.location)


class HappyHourLocation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=MAX_HAPPY_HOUR_LOCATION_LENGTH)

    def __str__(self):
        return "%s" % self.name


class UserFoodRating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=False)
    food = models.ForeignKey(SingleFood, on_delete=models.PROTECT)
    rating = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    class Meta:
        unique_together = ('user', 'food')

    def __str__(self):
        return "User: %s - Rating: %s" % (self.user.username, self.rating)


class UserFoodImage(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=False)
    food = models.ForeignKey(SingleFood, on_delete=models.PROTECT)
    image = models.ForeignKey('FoodImage', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('user', 'food')

    def __str__(self):
        return "User: %s - Image: %s" % (self.user.username, str(self.image))


class UserFoodComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=False)
    food = models.ForeignKey(SingleFood, on_delete=models.PROTECT)
    title = models.CharField(max_length=MAX_FOOD_COMMENT_TITLE_LENGTH, null=False, blank=False)
    description = models.CharField(max_length=MAX_FOOD_COMMENT_LENGTH, null=False, blank=False)

    class Meta:
        unique_together = ('user', 'food')

    def __str__(self):
        return "User: %s - Title: %s" % (self.user.username, self.title)


class FoodImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to=image_path, blank=False, null=False)
    thumb = models.ImageField(upload_to=thumb_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        image = Image.open(self.image)

        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')
        thumb_size = (128, 128)
        image.thumbnail(thumb_size, Image.ANTIALIAS)

        # save the thumbnail to memory
        temp_handle = BytesIO()
        image.save(temp_handle, 'jpeg')
        temp_handle.seek(0)  # rewind the file

        # save to the thumbnail field
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                 temp_handle.read(),
                                 content_type='image/jpg')

        # self.thumb.save('%s_thumbnail.%s' % (self.id, 'jpg'), suf, save=False)
        self.thumb.save(name='', content=suf, save=False)

        # save the image object
        super(FoodImage, self).save(*args, **kwargs)

    #
    # def delete(self, using=None, keep_parents=False):
    #     os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
    #     os.remove(os.path.join(settings.MEDIA_ROOT, self.thumb.name))
    #     super(FoodImage, self).delete()

    def __str__(self):
        return "Image: %s" % (str(self.image))
