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

router = routers.DefaultRouter()
router.register(r'all', views.FoodViewSet)
router.register(r'loc/(?P<location>.+)/$', views.FoodList.as_view(), base_name="food-on-loaction")
router.register(r'date/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.FoodList.as_view(),
                base_name="food-on-day")
# router.register(r'(?P<location>.+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.FoodList.as_view(), base_name="food-list")

urlpatterns = [
    url(r'^$', views.food, name='food'),
    # Daily Menus
    url(r'^daily/$', views.daily_food, name='daily-food'),
    url(r'^weekly/$', views.weekly_food, name='weekly-food'),
    url(r'^all/$', views.food, name='all-food'),
    url(r'^daily/rating/$', views.food_rating, name='rating-food'),
    url(r'^weekly/rating/$', views.food_rating, name='rating-food'),
    url(r'^api/', include(router.urls)),
    url(r'^api/(?P<location>[a-zA-Z]+)/$', views.FoodList.as_view(), name='rating-food'),
    url(r'^api/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.FoodList.as_view(),
        name='rating-food'),
    url(r'^api/(?P<location>[a-zA-Z]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
        views.FoodList.as_view(),
        name='rating-food'),
    url(r'^detail/(?P<id>[0-9]+)/$', views.food_detail, name='food-detail')
]
