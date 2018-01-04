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

from apps.food import views, admin_views
from django.conf.urls import url, include

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

    # Admin Pages
    url(r'^admin/$', admin_views.food_picture_management, name='foodpicture-management'),
    url(r'^admin/(?P<id>[0-9]+)/$', admin_views.food_picture_save, name='foodpicture-save'),
]
