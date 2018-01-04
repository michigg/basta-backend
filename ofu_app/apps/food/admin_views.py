# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import render
from pprint import pprint

from apps.food.models import Menu, SingleFood, UserFoodImage


def food_picture_management(request):
    if (request.user.is_superuser):
        today = datetime.datetime.now()
        today_images = UserFoodImage.objects.filter(food__foods__date__exact=today)

        return render(request, "admin/picture_management.jinja", {
            'day': today,
            'pictures': today_images,
        })

    else:
        return HttpResponseForbidden


def food_picture_save(request, id):
    if (request.user.is_superuser):
        chosen_pic = UserFoodImage.objects.get(id=id)
        food = SingleFood.objects.get(id=chosen_pic.food.id)
        food.image.set([chosen_pic, ])
        food.save()

        return food_picture_management(request)
    else:
        return HttpResponseForbidden
