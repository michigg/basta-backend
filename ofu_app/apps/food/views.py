# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.shortcuts import render

from apps.food.models import Menu, HappyHour, SingleFood
from django.http import HttpResponse


# Create your views here.
def daily_food(request):
    today = datetime.datetime.now() - datetime.timedelta(2)
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


def food_rating(request):
    food_id = request.GET.get('food_id', None)
    rating = request.GET.get('rating', None)
    if food_id and rating:
        print("ID: %s, RATING: %s" % (food_id, rating))
        food = SingleFood.objects.get(id=food_id)
        if rating == str(1):
            food.first_star = food.first_star + 1
        if rating == str(2):
            food.second_star += 1
        if rating == str(3):
            food.third_star += 1
        if rating == str(4):
            food.fourth_star += 1
        if rating == str(5):
            food.fifth_star += 1
        global_count = food.first_star + food.second_star + food.third_star + food.fourth_star + food.fifth_star
        sum = food.first_star * 1 + food.second_star * 2 + food.third_star * 3 + food.fourth_star * 4 + food.fifth_star * 5
        food.rating = sum / global_count
        print("SUMME: " + str(sum / global_count))
        food.save()
    return HttpResponse(status=200)
