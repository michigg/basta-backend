# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from api.serializers.food_serializers import MenuSerializer
from apps.food.models import Menu
from rest_framework import viewsets


class FoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
