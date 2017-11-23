from tkinter.constants import ALL

from apps.food.models import Menu, SingleFood, HappyHour, Allergene
from rest_framework import serializers


class AllergensSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Allergene
        fields = ('id', 'name')


class SingleFoodSerializer(serializers.HyperlinkedModelSerializer):
    allergens = AllergensSerializer(many=True, read_only=True)

    class Meta:
        model = SingleFood
        fields = ('name', 'rating', 'price_student', 'price_employee', 'price_guest', 'allergens')


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(format='iso-8601')
    menu = SingleFoodSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'date', 'location', 'menu')


class HappyHourSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(format='iso-8601')
    starttime = serializers.TimeField()
    endtime = serializers.TimeField()

    class Meta:
        model = HappyHour
        fields = ('id', 'date', 'starttime', 'endtime', 'location', 'description')
