# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from apps.food.models import UserFoodComment, UserFoodImage, UserFoodRating
from apps.registration.api.serializers import UserInformationSerializer, UserRatingSerializer, UserFoodImageSerializer, \
    UserCommentsSerializer
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


@permission_classes((IsAuthenticated,))
class UserInformations(generics.ListAPIView):
    serializer_class = UserInformationSerializer

    def get_queryset(self):
        return [self.request.user]


@permission_classes((IsAuthenticated,))
class UserRatings(generics.ListAPIView):
    serializer_class = UserRatingSerializer

    def get_queryset(self):
        user = self.request.user
        food_id = self.request.query_params.get('food_id')
        queryset = UserFoodRating.objects.filter(user=user).order_by('food__name')
        if food_id:
            try:
                queryset = queryset.filter(food_id=food_id)
            except ValueError as e:
                # TODO: return Exception
                return []

        return queryset


@permission_classes((IsAuthenticated,))
class UserImages(generics.ListAPIView):
    serializer_class = UserFoodImageSerializer

    def get_queryset(self):
        user = self.request.user
        food_id = self.request.query_params.get('food_id')
        queryset = UserFoodImage.objects.filter(user=user).order_by('food__name')
        if food_id:
            try:
                queryset = queryset.filter(food_id=food_id)
            except ValueError as e:
                # TODO: return Exception
                return []

        return queryset


@permission_classes((IsAuthenticated,))
class UserComments(generics.ListAPIView):
    serializer_class = UserCommentsSerializer

    def get_queryset(self):
        user = self.request.user
        food_id = self.request.query_params.get('food_id')
        queryset = UserFoodComment.objects.filter(user=user).order_by('food__name')
        if food_id:
            try:
                queryset = queryset.filter(food_id=food_id)
            except ValueError as e:
                # TODO: return Exception
                return []

        return queryset
