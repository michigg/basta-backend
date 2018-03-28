# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from datetime import timedelta

from apps.food.api.v1_1.serializers import MenuSerializer, HappyHourSerializer
from apps.food.models import Menu, HappyHour
from rest_framework import viewsets

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny


# @api_view(['GET'])
@permission_classes((AllowAny,))
class FoodViewSet(viewsets.ModelViewSet, ):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        queryset = Menu.objects.all()
        location = self.request.query_params.get('location')
        date = self.request.query_params.get('date')
        print(str(location).upper() == Menu.ERBA.upper())
        if location:
            print(str(location).upper() == Menu.ERBA.upper())
            if str(location).upper() is Menu.ERBA.upper():
                queryset = queryset.filter(location_contains='Erba')
            elif str(location).upper() is Menu.FEKI.upper():
                queryset = queryset.filter(location=Menu.FEKI)
            elif str(location).upper() is Menu.AUSTRASSE.upper():
                queryset = queryset.filter(location=Menu.AUSTRASSE)
            elif str(location).upper() is Menu.MARKUSPLATZ.upper():
                queryset = queryset.filter(location=Menu.MARKUSPLATZ)
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

        print("LOCATION: %s" % str(location))
        print("DATE: " + str(date))
        print(str(queryset))

        return queryset


# @api_view(['GET'])
@permission_classes((AllowAny,))
class FoodViewSetV1_1(viewsets.ModelViewSet, ):
    """
        API endpoint that allows users to be viewed or edited.
        """
    # queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        queryset = Menu.objects.all()
        location = None
        if 'location' in self.kwargs:
            location = self.kwargs['location']

        year = None
        if 'year' in self.kwargs:
            year = self.kwargs['year']
        month = None
        if 'month' in self.kwargs:
            month = self.kwargs['month']
        day = None
        if 'day' in self.kwargs:
            day = self.kwargs['day']

        if location:
            if str(location).upper() == Menu.ERBA.upper():
                queryset = queryset.filter(location__contains=Menu.ERBA)
            elif str(location).upper() == Menu.FEKI.upper():
                queryset = queryset.filter(location__contains=Menu.FEKI)
            elif str(location).upper() == Menu.AUSTRASSE.upper():
                print("Before: " + str(queryset))
                queryset = queryset.filter(location__contains=Menu.AUSTRASSE)
            elif str(location).upper() == Menu.MARKUSPLATZ.upper():
                queryset = queryset.filter(location__contains=Menu.MARKUSPLATZ)
        print(queryset)
        if year and month and day:
            date = '%s-%s-%s' % (year, month, day)
            queryset = queryset.filter(date=datetime.strptime(date, '%Y-%m-%d'))

        # if date == "week":
        #     today = datetime.now()
        #     weekday = today.weekday()
        #     monday = today - timedelta(weekday)
        #     sunday = today + (timedelta(6 - weekday))
        #     print("Monday: " + str(monday))
        #     print("Sunday: " + str(sunday))
        #     queryset = queryset.filter(date__gte=monday, date__lte=sunday)
        # else:
        #     queryset = queryset.filter(date=datetime.strptime(date, "%Y-%m-%d"))

        print("LOCATION: %s" % str(location))
        print(str(queryset))

        return queryset


# @api_view(['GET'])
@permission_classes((AllowAny,))
class FoodViewSetV1_1(viewsets.ModelViewSet, ):
    """
        API endpoint that allows users to be viewed or edited.
        """
    # queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        queryset = Menu.objects.all()
        location = None
        if 'location' in self.kwargs:
            location = self.kwargs['location']

        year = None
        if 'year' in self.kwargs:
            year = self.kwargs['year']
        month = None
        if 'month' in self.kwargs:
            month = self.kwargs['month']
        day = None
        if 'day' in self.kwargs:
            day = self.kwargs['day']

        if location:
            if str(location).upper() == Menu.ERBA.upper():
                queryset = queryset.filter(location__contains=Menu.ERBA)
            elif str(location).upper() == Menu.FEKI.upper():
                queryset = queryset.filter(location__contains=Menu.FEKI)
            elif str(location).upper() == Menu.AUSTRASSE.upper():
                print("Before: " + str(queryset))
                queryset = queryset.filter(location__contains=Menu.AUSTRASSE)
            elif str(location).upper() == Menu.MARKUSPLATZ.upper():
                queryset = queryset.filter(location__contains=Menu.MARKUSPLATZ)
        print(queryset)
        if year and month and day:
            date = '%s-%s-%s' % (year, month, day)
            queryset = queryset.filter(date=datetime.strptime(date, '%Y-%m-%d'))

        # if date == "week":
        #     today = datetime.now()
        #     weekday = today.weekday()
        #     monday = today - timedelta(weekday)
        #     sunday = today + (timedelta(6 - weekday))
        #     print("Monday: " + str(monday))
        #     print("Sunday: " + str(sunday))
        #     queryset = queryset.filter(date__gte=monday, date__lte=sunday)
        # else:
        #     queryset = queryset.filter(date=datetime.strptime(date, "%Y-%m-%d"))

        print("LOCATION: %s" % str(location))
        print(str(queryset))

        return queryset


# @api_view(['GET'])
@permission_classes((AllowAny,))
class HappyHourViewSet(viewsets.ModelViewSet):
    """
     API endpoint that allows users to be viewed or edited.
     """
    queryset = HappyHour.objects.all()
    serializer_class = HappyHourSerializer

    def get_queryset(self):
        queryset = HappyHour.objects.all()
        type = self.request.query_params.get('type')

        # if type == "food":
        #     queryset = HappyHour.filter(location__contains="Austraße")
        # elif type == "drinks":
        #     queryset = HappyHour.filter(location__contains="Austraße")

        return queryset
