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
from apps.food.api import views as api_views

urlpatterns = [
    # API Version 1.1
    url(r'^food/$', api_views.FoodViewSetV1_1.as_view({'get': 'list'})),
    url(r'^food/(?P<location>feldkirchenstrasse|markusstrasse|erba|austrasse)/$',
        api_views.FoodViewSetV1_1.as_view({'get': 'list'})),
    url(r'food/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
        api_views.FoodViewSetV1_1.as_view({'get': 'list'})),
    url(
        r'food/(?P<location>feldkirchenstrasse|markusstrasse|erba|austrasse)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
        api_views.FoodViewSetV1_1.as_view({'get': 'list'})),
    url(r'food/today/$', api_views.FoodViewSetV1_1.as_view({'get': 'list'})),
    url(r'food/week/$', api_views.FoodViewSetV1_1.as_view({'get': 'list'})),
    url(r'happy-hour', api_views.FoodViewSetV1_1.as_view({'get': 'list'})),
]
