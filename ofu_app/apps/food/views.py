# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.shortcuts import render

from apps.food.models import Menu, HappyHour


# Create your views here.
def daily_food(request):
    today = datetime.datetime.now()
    daily_menus = Menu.objects.filter(date__exact=today)
    feki_menu = daily_menus.filter(location__contains="Feldkirchenstraße").last()
    austr_menu = daily_menus.filter(location__contains="Austraße").last()
    erba_cafete = daily_menus.filter(location__contains="Erba").last()
    markus_cafete = daily_menus.filter(location__contains="markus").last()
    happy_hours = HappyHour.objects.filter(date__exact=today)
    print(feki_menu.menu)
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
    lastday = datetime.datetime.now() + datetime.timedelta(7)
    weekly_menus = Menu.objects.filter(date__gte=today, date__lte=lastday)
    feki_menu = weekly_menus.filter(location__contains="Feldkirchenstraße")
    austr_menu = weekly_menus.filter(location__contains="Austraße")
    erba_cafete = weekly_menus.filter(location__contains="Erba")
    markus_cafete = weekly_menus.filter(location__contains="markus")
    happy_hours = HappyHour.objects.filter(date__gte=today, date__lte=lastday)
    print(feki_menu.menu)
    return render(request, "food/daily_food.jinja", {
        'day': today,
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
    return render(request, "food/food.jinja", {
    })
