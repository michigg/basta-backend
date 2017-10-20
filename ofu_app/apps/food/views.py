# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.shortcuts import render

from apps.food.models import Menu, HappyHour, SingleFood


# Create your views here.
def daily_food(request):
    print(
        "REQUEST------------------------------------------------------------------------------------------------------")
    id = request.GET.get('food_id', None)
    rating = request.GET.get('rating', None)
    print("ID: %s, RATING: %s" % (id, rating))
    if id and rating:
        food = SingleFood.objects.get(id=id)
        food.rating = rating
        food.save()
        print("DONE")

    today = datetime.datetime.now()
    daily_menus = Menu.objects.filter(date__exact=today)
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
