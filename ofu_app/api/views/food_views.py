# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from datetime import timedelta
from api.serializers.food_serializers import MenuSerializer
from apps.food.models import Menu
from rest_framework import viewsets
from django.http import JsonResponse


class FoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        queryset = Menu.objects.all()
        location = self.request.query_params.get('location')
        date = self.request.query_params.get('date')

        if location:
            locations = ["erba", "feldkirchenstrasse", "austrasse", "markusplatz"]
            if locations.__contains__(location):
                if location == locations[0]:
                    queryset = queryset.filter(location__contains="Erba")
                elif location == locations[1]:
                    queryset = queryset.filter(location__contains="Feldkirchen")
                elif location == locations[2]:
                    queryset = queryset.filter(location__contains="Austraße")
                elif location == locations[3]:
                    queryset = queryset.filter(location__contains="Markusplatz")
        if date:
            if date == "week":
                today = datetime.now()
                weekday = today.weekday()
                monday = today - timedelta(weekday)
                sunday = today + (timedelta(6 - weekday))
                print("Monday: " + str(monday))
                print("Sunday: " + str(sunday))
                queryset = queryset.filter(date__gte=monday, date__lte=sunday)
            else:
                queryset = queryset.filter(date=datetime.strptime(date, "%Y-%m-%d"))

        print("DATE: " + date)
        print(str(queryset))

        return queryset
