"""ofu_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers

from apps.food import views
from apps.food.api import views as api_views

# API Version 1.0
apiRouter_v1 = routers.DefaultRouter()
apiRouter_v1.register(r'food', api_views.FoodViewSet, base_name='Food')
apiRouter_v1.register(r'happy-hour', api_views.HappyHourViewSet, base_name='HappyHours')

# API Version 1.1
apiRouter_v1_1 = routers.DefaultRouter()
apiRouter_v1_1.register(r'foods', api_views.FoodViewSet, base_name='Food')
apiRouter_v1_1.register(r'foods/food/(?P<location>[feldkirchenstrasse, markusstrasse, erba, austrasse])/$',
                        api_views.FoodViewSet, base_name='Food')
apiRouter_v1_1.register(r'foods/food/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', api_views.FoodViewSet,
                        base_name='Food')
apiRouter_v1_1.register(
    r'foods/food/(?P<location>)[feldkirchenstrasse, markusstrasse, erba, austrasse]/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
    api_views.FoodViewSet, base_name='Food')
apiRouter_v1_1.register(r'foods/food/today/$', api_views.FoodViewSet, base_name='Food')
apiRouter_v1_1.register(r'foods/food/week/$', api_views.FoodViewSet, base_name='Food')
apiRouter_v1_1.register(r'happy-hour', api_views.HappyHourViewSet, base_name='HappyHours')

urlpatterns = [
    url(r'^$', views.food, name='food'),

    # Daily Menus
    url(r'^daily/$', views.daily_food, name='daily-food'),

    # Weekly Menus
    url(r'^weekly/$', views.weekly_food, name='weekly-food'),

    # All known Menus
    # url(r'^all/$', views.food, name='all-food'),

    # Food detailed
    url(r'^(?P<id>[0-9]+)/$', views.food_detail, name='food-detail'),

    # Food Rating
    url(r'^daily/rating/$', views.food_rating, name='rating-food'),
    url(r'^weekly/rating/$', views.food_rating, name='rating-food'),

]
