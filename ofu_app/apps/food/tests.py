# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from apps.food.models import SingleFood


# Create your tests here.

class SingleFood_Created_Just_with_name(TestCase):
    def setUp(self):
        SingleFood.objects.create(name="testfood")

    def test_food_created_just_with_name(self):
        """Animals that can speak are correctly identified"""
        food = SingleFood.objects.get(name="testfood")
        self.assertEqual(food.name, 'testfood')
        self.assertIsNone(food.allergens.all().first(), [])
        self.assertIsNone(food.price_employee)
        self.assertIsNone(food.price_guest)
        self.assertIsNone(food.price_student)
        self.assertIsNone(food.image)
        self.assertEqual(food.rating, 0.0)
