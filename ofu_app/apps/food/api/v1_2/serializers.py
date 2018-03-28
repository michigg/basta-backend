from rest_framework import serializers

from apps.food.models import Menu, SingleFood, HappyHour, Allergene, FoodImage, HappyHourLocation
from apps.food.models import UserFoodRating, UserFoodImage
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import validators


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

    class Meta:
        model = SingleFood
        fields = ('id', 'name', 'rating', 'price_student', 'price_employee', 'price_guest', 'allergens', 'image')


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


# --------------------------- User --------------------------------------------
class UserFoodImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserFoodImage
        fields = ('id', 'image_image', 'image_thumb')


class UserFoodRatingSerializer(serializers.ModelSerializer):
    # food = MinimalSingleFoodSerializer(many=False, read_only=False)

    class Meta:
        model = UserFoodRating
        fields = ('id', 'rating')

    def run_validators(self, value):
        for validator in self.validators:
            if isinstance(validator, validators.UniqueTogetherValidator):
                self.validators.remove(validator)
        super(UserFoodRatingSerializer, self).run_validators(value)

    def create(self, validated_data):
        # TODO: Custom exception handler
        rating = validated_data.pop('rating')
        if rating >= 1 or rating <= 5:
            food_id = self.context.get('food_id')
            # user = self.context['request'].user
            user = User.objects.get(id=1)
            food = SingleFood.objects.get(id=food_id)
            user_rating, _ = UserFoodRating.objects.get_or_create(food=food, user=user)
            user_rating.rating = rating
            user_rating.save()

            food_user_ratings = UserFoodRating.objects.all().filter(food=food)
            sum = 0
            for food_user_rating in food_user_ratings:
                sum += food_user_rating.rating

            food.rating = sum / food_user_ratings.count()
            food.save()
            return user_rating
        else:
            raise ValueError
