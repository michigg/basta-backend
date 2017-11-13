from apps.food.models import Menu, SingleFood, HappyHour
from rest_framework import serializers


class SingleFoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SingleFood
        fields = ('name', 'rating')


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(format='iso-8601')
    menu = SingleFoodSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ('date', 'location', 'menu')


class HappyHourSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(format='iso-8601')
    starttime = serializers.TimeField()
    endtime = serializers.TimeField()

    class Meta:
        model = HappyHour
        fields = ('date', 'starttime', 'endtime', 'location', 'description')
