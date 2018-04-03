from rest_framework import serializers
from django.contrib.auth.models import User
from apps.food.models import UserFoodRating, UserFoodImage, UserFoodComment, SingleFood, FoodImage
from apps.food.api.v1_2.serializers.main_serializers import MinimalSingleFoodSerializer


class FoodImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodImage
        fields = ('image', 'thumb')


class UserFoodImageSerializer(serializers.HyperlinkedModelSerializer):
    image = FoodImageSerializer(many=False, read_only=True)
    food = MinimalSingleFoodSerializer(many=False, read_only=True)

    class Meta:
        model = UserFoodImage
        fields = ('id', 'food', 'image')


class SingleFoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SingleFood
        fields = ('id', 'name')


class UserFoodImagesSerializer(serializers.HyperlinkedModelSerializer):
    food = SingleFoodSerializer(many=False, read_only=True)

    class Meta:
        model = UserFoodImage
        fields = ('id', 'food', 'image_image', 'image_thumb')


class UserRatingSerializer(serializers.HyperlinkedModelSerializer):
    food = SingleFoodSerializer(many=False, read_only=True)

    class Meta:
        model = UserFoodRating
        fields = ('id', 'food', 'rating')


class UserCommentsSerializer(serializers.HyperlinkedModelSerializer):
    food = SingleFoodSerializer(many=False, read_only=True)

    class Meta:
        model = UserFoodComment
        fields = ('id', 'food', 'description', 'title')


class UserInformationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login')
