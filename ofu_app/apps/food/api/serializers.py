from rest_framework import serializers

from apps.food.models import Menu, SingleFood, HappyHour, Allergene, UserFoodImage, FoodImage


class UserFoodImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserFoodImage
        fields = ('id', 'image_image', 'image_thumb')


class FoodImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodImage
        fields = ('id', 'image', 'thumb')


class AllergensSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Allergene
        fields = ('id', 'name')


class SingleFoodSerializer(serializers.HyperlinkedModelSerializer):
    allergens = AllergensSerializer(many=True, read_only=True)
    image = FoodImageSerializer(many=False, read_only=True)

    class Meta:
        model = SingleFood
        fields = ('name', 'rating', 'price_student', 'price_employee', 'price_guest', 'allergens', 'image')


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(format='iso-8601')
    menu = SingleFoodSerializer(many=True, read_only=True)
    location = serializers.ChoiceField(choices=Menu.LOCATION_CHOICES)

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
