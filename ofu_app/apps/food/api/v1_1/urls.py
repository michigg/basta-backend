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
from django.conf.urls import url
from apps.food.api.v1_1 import views as api_views
from apps.food.models import Menu

urlpatterns = [
    # API Version 1.1
    url(r'^food/$', api_views.FoodViewSetV1_1.as_view({'get': 'list'}), name='api-v1_1-food-all'),
    url(r'^food/(?P<location>' + Menu.FEKI + '|' + Menu.MARKUSPLATZ + '|' + Menu.ERBA + '|' + Menu.AUSTRASSE + ')/$',
        api_views.FoodViewSetV1_1.as_view({'get': 'list'}), name='api-v1_1-food-location'),
    url(r'food/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
        api_views.FoodViewSetV1_1.as_view({'get': 'list'}), name='api-v1_1-food-date'),
    url(
        r'food/(?P<location>' + Menu.FEKI + '|' + Menu.MARKUSPLATZ + '|' + Menu.ERBA + '|' + Menu.AUSTRASSE + ')/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
        api_views.FoodViewSetV1_1.as_view({'get': 'list'}), name='api-v1_1-food-location-date'),
    url(r'food/today/$', api_views.FoodViewSetV1_1.as_view({'get': 'list'}), name='api-v1_1-food-today'),
    url(r'food/week/$', api_views.FoodViewSetV1_1.as_view({'get': 'list'}), name='api-v1_1-food-week'),
    url(r'happy-hour', api_views.HappyHourViewSet.as_view({'get': 'list'}), name='api-v1_1-happy-hour-all'),
]
