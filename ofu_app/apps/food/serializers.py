from apps.food.models import Menu, SingleFood
from rest_framework import serializers


class SingleFoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SingleFood
        fields = ('name',)


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(format='iso-8601')
    menu = SingleFoodSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ('date', 'location', 'menu')
