from apps.food.models import Menu, SingleFood
from apps.food.models import UserFoodRating, UserFoodImage, UserFoodComment, FoodImage
from django.contrib.auth.models import User
from rest_framework import validators
from rest_framework import serializers
from django.db.utils import IntegrityError
import logging

logger = logging.getLogger(__name__)


class UserFoodImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserFoodImage
        fields = ('id', 'image_image', 'image_thumb')


class UserFoodCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFoodComment
        fields = ('id', 'title', 'description')

    def run_validators(self, value):
        for validator in self.validators:
            if isinstance(validator, validators.UniqueTogetherValidator):
                self.validators.remove(validator)
        super(UserFoodCommentSerializer, self).run_validators(value)

    def create(self, validated_data):
        comment_title = validated_data.pop('title')
        comment_description = validated_data.pop('description')
        food_id = self.context.get('food_id')
        user = self.context['request'].user
        food = SingleFood.objects.get(id=food_id)

        user_comment, _ = UserFoodComment.objects.get_or_create(food=food, user=user)
        user_comment.title = comment_title
        user_comment.description = comment_description
        user_comment.save()
        return user_comment


class UserFoodRatingSerializer(serializers.ModelSerializer):
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
            user = self.context['request'].user
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


class UserFoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImage
        fields = ('id', 'image')

    def run_validators(self, value):
        for validator in self.validators:
            if isinstance(validator, validators.UniqueTogetherValidator):
                self.validators.remove(validator)
        super(UserFoodImageSerializer, self).run_validators(value)

    def create(self, validated_data):
        # TODO: Custom exception handler
        food_id = self.context.get('food_id')
        food = SingleFood.objects.get(id=food_id)
        user = self.context['request'].user
        image = validated_data.pop('image')
        food_image = FoodImage.objects.create(image=image)
        food_image.save()
        logger.info('New Image: {}\nFood: {}'.format(food_image.image.url, food.name))
        logger.error('New Image: {}\nFood: {}'.format(food_image.image.url, food.name))
        try:
            user_food_image = UserFoodImage.objects.create(user=user, food=food, image=food_image)
            user_food_image.save()
        except IntegrityError as err:
            user_food_image = UserFoodImage.objects.get(user=user, food=food)
            user_food_image.image = food_image
            user_food_image.save()
        return food_image
