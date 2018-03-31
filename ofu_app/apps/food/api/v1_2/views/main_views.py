# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.templatetags.static import static

from datetime import datetime
from datetime import timedelta

from apps.food.api.v1_2.serializers.main_serializers import OverviewMenuSerializer, DetailMenuSerializer, \
    MenusLocationsSerializer
from apps.food.api.v1_2.serializers.main_serializers import OverviewSingleFoodSerializer, DetailedSingleFoosdSerializer, \
    AllergensSerializer, DetailedFoodImageSerializer, DefaultFoodImageSerializer, MinimalSingleFoodSerializer, \
    UserFoodCommentSerializer
from apps.food.api.v1_2.serializers.main_serializers import HappyHourSerializer, HappyHourLocationSerializer
from apps.food.models import Menu, SingleFood, Allergene, HappyHour, HappyHourLocation, FoodImage, UserFoodRating, \
    UserFoodComment
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


@permission_classes((AllowAny,))
class ApiMenus(generics.ListAPIView):
    serializer_class = OverviewMenuSerializer

    def get_queryset(self):
        queryset = Menu.objects.all()
        location = self.request.query_params.get('location')
        start_date = self.request.query_params.get('startdate')
        end_date = self.request.query_params.get('enddate')

        if location:
            if str(location).upper() == Menu.ERBA.upper():
                queryset = queryset.filter(location__contains=Menu.ERBA)
            elif str(location).upper() == Menu.FEKI.upper():
                queryset = queryset.filter(location__contains=Menu.FEKI)
            elif str(location).upper() == Menu.AUSTRASSE.upper():
                queryset = queryset.filter(location__contains=Menu.AUSTRASSE)
            elif str(location).upper() == Menu.MARKUSPLATZ.upper():
                queryset = queryset.filter(location__contains=Menu.MARKUSPLATZ)
            else:
                queryset = []
        if start_date:
            try:
                queryset = queryset.filter(date__gte=datetime.strptime(start_date, '%Y-%m-%d'))
            except ValueError as e:
                # TODO: return Exception
                return []

        if end_date:
            try:
                queryset = queryset.filter(date__lte=datetime.strptime(end_date, '%Y-%m-%d'))
            except ValueError as e:
                # TODO: return Exception
                return []

        return queryset


@permission_classes((AllowAny,))
class ApiMenu(generics.RetrieveAPIView):
    serializer_class = DetailMenuSerializer
    queryset = Menu.objects.all()


@permission_classes((AllowAny,))
class ApiMeals(generics.ListAPIView):
    serializer_class = OverviewSingleFoodSerializer

    def get_queryset(self):
        queryset = SingleFood.objects.all()
        rating = self.request.query_params.get('rating')
        max_rating = self.request.query_params.get('max-rating')
        min_rating = self.request.query_params.get('min-rating')

        price = self.request.query_params.get('price')
        max_price = self.request.query_params.get('max-price')
        min_price = self.request.query_params.get('min-price')

        allergens = self.request.query_params.get('allergens')

        if rating:
            queryset = queryset.filter(rating=rating)

        if max_rating:
            queryset = queryset.filter(rating__lte=max_rating)

        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        # TODO: Change price model to Floatfield
        # if price:
        #     pass
        #
        # if max_price:
        #     pass
        #
        # if min_price:
        #     pass

        if allergens:
            allergens = [allergen for allergen in str(allergens).strip('[]').split(',')]
            queryset = queryset.filter(allergens__id__in=allergens)

        return queryset


@permission_classes((AllowAny,))
class ApiMeal(generics.RetrieveAPIView):
    serializer_class = DetailedSingleFoosdSerializer
    queryset = SingleFood.objects.all()


@permission_classes((AllowAny,))
class ApiAllergens(generics.ListAPIView):
    serializer_class = AllergensSerializer
    queryset = Allergene.objects.all()


@permission_classes((AllowAny,))
class ApiMenusLocations(views.APIView):

    def get(self, request):
        locations = Menu.API_LOCATIONS
        results = MenusLocationsSerializer(locations, many=True).data
        return Response(results, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class ApiMealComments(generics.ListAPIView):
    serializer_class = UserFoodCommentSerializer

    def get_queryset(self):
        food_id = self.kwargs['pk']
        return UserFoodComment.objects.filter(food_id=food_id)


@permission_classes((AllowAny,))
class ApiHappyHours(generics.ListAPIView):
    serializer_class = HappyHourSerializer

    def get_queryset(self):
        queryset = HappyHour.objects.all()
        date = self.request.query_params.get('date')
        start_date = self.request.query_params.get('startdate')
        end_date = self.request.query_params.get('enddate')

        start_time = self.request.query_params.get('starttime')
        end_time = self.request.query_params.get('endtime')

        location = self.request.query_params.get('location')
        if date:
            try:
                queryset = queryset.filter(date=datetime.strptime(date, '%Y-%m-%d'))
            except ValueError as e:
                # TODO: return Exception
                return []

        if start_date:
            try:
                queryset = queryset.filter(date__gte=datetime.strptime(start_date, '%Y-%m-%d'))
            except ValueError as e:
                # TODO: return Exception
                return []

        if end_date:
            try:
                queryset = queryset.filter(date__lte=datetime.strptime(start_date, '%Y-%m-%d'))
            except ValueError as e:
                # TODO: return Exception
                return []

        if start_time:
            try:
                queryset = queryset.filter(date__lte=datetime.strptime(start_time, '%H'))
            except ValueError as e:
                # TODO: return Exception
                return []

        if end_time:
            try:
                queryset = queryset.filter(date__lte=datetime.strptime(end_time, '%H'))
            except ValueError as e:
                # TODO: return Exception
                return []

        if location:
            queryset = queryset.filter(location__id=location)

        return queryset


@permission_classes((AllowAny,))
class ApiHappyHoursLocations(generics.RetrieveAPIView):
    serializer_class = HappyHourSerializer
    queryset = HappyHour.objects.all()


@permission_classes((AllowAny,))
class ApiHappyHoursLocations(generics.ListAPIView):
    serializer_class = HappyHourLocationSerializer
    queryset = HappyHourLocation.objects.all()


@permission_classes((AllowAny,))
class ApiFoodImages(generics.ListAPIView):
    serializer_class = DetailedFoodImageSerializer
    queryset = FoodImage.objects.all()


@permission_classes((AllowAny,))
class ApiFoodImagesDefault(views.APIView):

    def get(self, request):
        request.build_absolute_uri(static('img/food/default.jpg'))
        default_image = {'image': request.build_absolute_uri(static('img/food/default.jpg'))}
        results = DefaultFoodImageSerializer(default_image, many=False).data
        return Response(results, status=status.HTTP_200_OK)
