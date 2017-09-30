# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.shortcuts import render

from apps.food import Menu, HappyHour


# Create your views here.
def daily_food(request):
    today = datetime.datetime.now()
    daily_menus = Menu.objects.filter(date__exact=today)
    feki_menu = daily_menus.filter(location__contains="Feldkirchenstraße").last()
    austr_menu = daily_menus.filter(location__contains="Austraße").last()
    erba_cafete = daily_menus.filter(location__contains="Erba").last()
    markus_cafete = daily_menus.filter(location__contains="markus").last()
    happy_hours = HappyHour.objects.filter(date__exact=today)
    return render(request, "food/daily_food.jinja", {
        'day': today,
        'happy_hours': happy_hours,
        'feki_menu': feki_menu,
        'austr_menu': austr_menu,
        'erba_cafete': erba_cafete,
        'markus_cafete': markus_cafete,
    })


def food(request):
    return render(request, "food/food.jinja", {
    })
