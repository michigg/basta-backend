from apps.food.models import Menu, SingleFood, HappyHour, Allergene, FoodImage, HappyHourLocation, UserFoodComment
from rest_framework import serializers


class DefaultFoodImageSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    image = serializers.CharField()


class MenusLocationsSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    id = serializers.CharField()
    short = serializers.CharField()
    name = serializers.CharField()


class UserFoodCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserFoodComment
        fields = ('id', 'description', 'title')


class AllergensSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Allergene
        fields = ('id', 'name')


class OverviewFoodImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodImage
        fields = ('id', 'thumb')


class DetailedFoodImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodImage
        fields = ('id', 'image', 'thumb')


class OverviewSingleFoodSerializer(serializers.HyperlinkedModelSerializer):
    image = OverviewFoodImageSerializer(many=False, read_only=True)

    class Meta:
        model = SingleFood
        fields = ('id', 'name', 'rating', 'price_student', 'image')


class MinimalSingleFoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SingleFood
        fields = ('id', 'name')


class DetailedSingleFoosdSerializer(serializers.HyperlinkedModelSerializer):
    allergens = AllergensSerializer(many=True, read_only=True)
    image = DetailedFoodImageSerializer(many=False, read_only=True)
    comments = UserFoodCommentSerializer(many=True, read_only=True)

    class Meta:
        model = SingleFood
        fields = (
            'id', 'name', 'rating', 'price_student', 'price_employee', 'price_guest', 'allergens', 'image', 'comments')


class OverviewMenuSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(format='iso-8601')
    menu = OverviewSingleFoodSerializer(many=True, read_only=True)
    location = serializers.ChoiceField(choices=Menu.LOCATION_CHOICES)

    class Meta:
        model = Menu
        fields = ('id', 'date', 'location', 'menu')


class DetailMenuSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(format='iso-8601')
    menu = DetailedSingleFoosdSerializer(many=True, read_only=True)
    location = serializers.ChoiceField(choices=Menu.LOCATION_CHOICES)

    class Meta:
        model = Menu
        fields = ('id', 'date', 'location', 'menu')


# --------------------------  Happy Hour  ------------------------------------
class HappyHourSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(format='iso-8601')
    starttime = serializers.TimeField()
    endtime = serializers.TimeField()

    class Meta:
        model = HappyHour
        fields = ('id', 'date', 'starttime', 'endtime', 'location', 'description')


class HappyHourLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HappyHourLocation
        fields = ('id', 'name')
