# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils import timezone
from django.utils.encoding import smart_str

MAX_LENGTH = 256


# Create your models here.
class Menu(models.Model):
    ERBA = 'ERBA'
    MARKUSPLATZ = 'MARKUSPLATZ'
    FEKI = 'FEKI'
    AUSTRASSE = 'AUSTRASSE'

    LOCATION_CHOICES = (
        (ERBA, 'Erba'), (MARKUSPLATZ, 'Markusplatz'), (FEKI, 'Feldkirchenstrasse'), (AUSTRASSE, 'Austrasse'))
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=MAX_LENGTH, choices=LOCATION_CHOICES)
    menu = models.ManyToManyField("SingleFood", related_name="foods")

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
    image = models.ManyToManyField("UserFoodImage", blank=True, null=True)
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
        # TODO: unique description instead of date
        unique_together = ('date', 'location', 'starttime', 'endtime')

    def __str__(self):
        return "Date: %s, Location: %s" % (self.date.strftime("%Y.%m.%d"), self.location)


class UserRating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=False)
    food = models.ForeignKey(SingleFood, on_delete=models.PROTECT)
    rating = models.FloatField(default=0)

    def __str__(self):
        return "User: %s - Rating: %s" % (self.user.username, self.rating)


class UserFoodImage(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=False)
    food = models.ForeignKey(SingleFood, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='food/originals/%Y/%m/%W', blank=True)
    thumb = models.ImageField(upload_to='food/thumbs/%Y/%m/%W', blank=True)

    class Meta:
        unique_together = ('user', 'food')

    def __str__(self):
        return "User: %s - Image: %s" % (self.user.username, str(self.image))

    def save(self, force_update=False, force_insert=False, thumb_size=(640, 480)):
        image = Image.open(self.image)

        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')
        image.thumbnail(thumb_size, Image.ANTIALIAS)

        # save the thumbnail to memory
        temp_handle = BytesIO()
        image.save(temp_handle, 'jpeg')
        temp_handle.seek(0)  # rewind the file

        # save to the thumbnail field
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                 temp_handle.read(),
                                 content_type='image/jpg')

        str_food = smart_str(self.food.name, encoding='utf-8')
        self.thumb.save('%s_%s_thumbnail.%s' % (str_food, self.user.id, 'jpg'), suf, save=False)
        # save the image object
        self.image.name = "%s_%s_original.%s" % (str_food, self.user.id, 'jpg')
        super(UserFoodImage, self).save(force_update, force_insert)

    def delete(self, using=None, keep_parents=False):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        os.remove(os.path.join(settings.MEDIA_ROOT, self.thumb.name))
        super(UserFoodImage, self).delete()
