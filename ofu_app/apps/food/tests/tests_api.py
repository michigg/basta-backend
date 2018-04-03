# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from apps.food.models import SingleFood, Menu
from apps.food.api.v1_1.serializers import MenuSerializer
from rest_framework import status

from datetime import datetime


# Create your tests here.

class SingleFood_Scope(TestCase):
    def setUp(self):
        self.singlefood_1 = SingleFood.objects.create(name="testfood1")
        self.singlefood_2 = SingleFood.objects.create(name="testfood2")
        self.singlefood_3 = SingleFood.objects.create(name="testfood3")
        self.singlefood_4 = SingleFood.objects.create(name="testfood4")
        self.singlefood_5 = SingleFood.objects.create(name="testfood5")
        self.singlefood_6 = SingleFood.objects.create(name="testfood6")
        self.today_menu = Menu.objects.create(date='2017-01-15', location=Menu.ERBA)
        self.today_menu.menu.add(self.singlefood_1)
        self.today_menu.menu.add(self.singlefood_2)
        self.today_menu.menu.add(self.singlefood_3)
        self.menu_2 = Menu.objects.create(date='2017-01-10', location=Menu.FEKI)
        self.menu_2.menu.add(self.singlefood_4)
        self.menu_2.menu.add(self.singlefood_5)
        self.menu_2.menu.add(self.singlefood_6)

    def test_get_food_root(self):
        """
        All menus in response
        """
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        response = self.client.get(reverse('api-v1_1-food-all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_food_date_param(self):
        """
        Menu for a given date is in the response
        """
        serializer = MenuSerializer(self.menu_2, many=False)
        response_1 = self.client.get(reverse('api-v1_1-food-date', kwargs={'year': '2017', 'month': '01', 'day': '10'}))
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.data, [serializer.data])

        serializer_2 = MenuSerializer(self.today_menu, many=False)
        response_2 = self.client.get(reverse('api-v1_1-food-date', kwargs={'year': '2017', 'month': '01', 'day': '15'}))
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_2.data, [serializer_2.data])

    def test_get_food_date_param_not_in_set(self):
        """
        Empty response if no object with request date in set
        """
        response_1 = self.client.get(reverse('api-v1_1-food-date', kwargs={'year': '2017', 'month': '01', 'day': '11'}))
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.data, [])

    def test_get_food_location_param(self):
        """
        Menu for a given location is in the response
        """
        serializer_1 = MenuSerializer(self.today_menu, many=False)
        response_1 = self.client.get(reverse('api-v1_1-food-location', kwargs={'location': Menu.ERBA}))
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.data, [serializer_1.data])

        serializer_2 = MenuSerializer(self.menu_2, many=False)
        response_2 = self.client.get(reverse('api-v1_1-food-location', kwargs={'location': Menu.FEKI}))
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_2.data, [serializer_2.data])

    def test_get_food_location_param_not_in_set(self):
        """
        Empty response if no object with request location in set
        """
        response_1 = self.client.get(reverse('api-v1_1-food-location', kwargs={'location': Menu.AUSTRASSE}))
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.data, [])

    def test_get_food_location_date_param(self):
        """
        Menu for request location and date is in the response
        """

        serializer = MenuSerializer(self.menu_2, many=False)
        response = self.client.get(reverse('api-v1_1-food-location-date',
                                           kwargs={'year': '2017', 'month': '01', 'day': '10',
                                                   'location': Menu.FEKI}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [serializer.data])

    def test_get_food_location_date_param_not_in_set(self):
        """
        Empty response if no object with request date and location in set
        """
        response_1 = self.client.get(reverse('api-v1_1-food-location-date',
                                             kwargs={'year': '2017', 'month': '01', 'day': '11',
                                                     'location': Menu.FEKI}))
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.data, [])

        response_1 = self.client.get(reverse('api-v1_1-food-location-date',
                                             kwargs={'year': '2017', 'month': '01', 'day': '10',
                                                     'location': Menu.AUSTRASSE}))
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.data, [])

    def test_get_food_today_param(self):
        """
        Menu for request today is in the response
        """
        self.singlefood = SingleFood.objects.create(name="testfood")
        self.today_menu = Menu.objects.create(date=datetime.today().strftime('%Y-%m-%d'), location=Menu.ERBA)
        self.today_menu.menu.add(self.singlefood)

        serializer = MenuSerializer(self.today_menu, many=False)
        response = self.client.get(reverse('api-v1_1-food-today'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [serializer.data])

    def test_get_food_today_param_not_in_set(self):
        """
        Empty response if no object with date 'today' is in set
        """
        response = self.client.get(reverse('api-v1_1-food-today'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
