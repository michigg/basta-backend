# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from pprint import pprint

from apps.food.forms import UploadImageForm
from apps.food.models import Menu, HappyHour, SingleFood, UserRating, UserFoodImage


# Create your views here.
def daily_food(request):
    today = datetime.datetime.now() - datetime.timedelta(4)
    feki_menu = Menu.objects.filter(date__exact=today).filter(location__contains="Feldkirchenstraße").last()
    austr_menu = Menu.objects.filter(date__exact=today).filter(location__contains="Austraße").last()
    erba_cafete = Menu.objects.filter(date__exact=today).filter(location__contains="Erba").last()
    markus_cafete = Menu.objects.filter(date__exact=today).filter(location__contains="markus").last()
    happy_hours = HappyHour.objects.filter(date__exact=today)

    return render(request, "food/daily_food.jinja", {
        'day': today,
        'happy_hours': happy_hours,
        'feki_menu': feki_menu,
        'austr_menu': austr_menu,
        'erba_cafete': erba_cafete,
        'markus_cafete': markus_cafete,
    })


def weekly_food(request):
    today = datetime.datetime.now()
    lastday = today + datetime.timedelta(7)
    weekly_menus = Menu.objects.filter(date__gte=today, date__lte=lastday)
    feki_menu = weekly_menus.filter(location__contains="Feldkirchenstraße")
    austr_menu = weekly_menus.filter(location__contains="Austraße")
    erba_cafete = weekly_menus.filter(location__contains="Erba")
    markus_cafete = weekly_menus.filter(location__contains="markus")
    happy_hours = HappyHour.objects.filter(date__gte=today, date__lte=lastday)
    return render(request, "food/weekly_food.jinja", {
        'day': today,
        'lastday': lastday,
        'happy_hours': happy_hours,
        'feki_menu': feki_menu,
        'austr_menu': austr_menu,
        'erba_cafete': erba_cafete,
        'markus_cafete': markus_cafete,
    })


def food_detail(request, id):
    if request.method == 'POST':
        if pic_upload(request, id) == False:
            return HttpResponse(status=404)
    food = SingleFood.objects.get(id=id)
    images = UserFoodImage.objects.filter(food=id)
    return render(request, "food/detailed_food.jinja", {'food': food, 'images': images})


def all_food(request):
    menus = Menu.objects.all()
    feki_menu = menus.filter(location__contains="Feldkirchenstraße")
    austr_menu = menus.filter(location__contains="Austraße")
    erba_cafete = menus.filter(location__contains="Erba")
    markus_cafete = menus.filter(location__contains="markus")
    happy_hours = HappyHour.objects.all()
    return render(request, "food/daily_food.jinja", {
        'happy_hours': happy_hours,
        'feki_menu': feki_menu,
        'austr_menu': austr_menu,
        'erba_cafete': erba_cafete,
        'markus_cafete': markus_cafete,
    })


def food(request):
    return render(request, "food/home.jinja", {
    })


def food_rating(request):
    if (request.user.is_authenticated):
        food_id = request.GET.get('food_id', None)
        rating = request.GET.get('rating', None)
        if food_id and rating:
            food = SingleFood.objects.get(id=food_id)
            user_rating, created = UserRating.objects.get_or_create(user=request.user,
                                                                    food=food)
            user_rating.rating = rating
            user_rating.save()

            food_user_ratings = UserRating.objects.all().filter(food=food)
            sum = 0
            for food_user_rating in food_user_ratings:
                sum += food_user_rating.rating

            food.rating = sum / food_user_ratings.count()
            food.save()
            return HttpResponse(status=200)
        return HttpResponse(status=404)
    return HttpResponse(status=403)


def food_image(request):
    food_id = request.GET.get('food_id', None)
    img = request.GET.get('img', None)
    if food_id and img:
        food = SingleFood.objects.get(id=food_id)
        food.image = img
        food.save()
        return HttpResponse(status=200)
    return HttpResponse(status=404)


def pic_upload(request, id):
    form = UploadImageForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            old_user_pic = UserFoodImage.objects.get(user=request.user, food=id)
            old_user_pic.delete()
            os.remove(os.path.join(settings.MEDIA_ROOT, old_user_pic.image.name))
        except ObjectDoesNotExist:
            pass
        userPic = form.save(commit=False)
        userPic.food = SingleFood.objects.get(id=id)
        userPic.user = request.user
        userPic.save()
        return True
    else:
        return False
