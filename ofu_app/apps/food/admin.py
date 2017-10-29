# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from apps.food.models import SingleFood, Menu, HappyHour, UserRating

# Register your models here.
admin.site.register(SingleFood)
admin.site.register(Menu)
admin.site.register(HappyHour)
admin.site.register(UserRating)

