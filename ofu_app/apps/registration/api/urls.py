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
from apps.registration.api import views as api_views
from apps.food.models import Menu

urlpatterns = [
    # API Version 1.1
    url(r'^account/$', api_views.UserInformations.as_view(), name='api-v1_1-user-information'),
    url(r'^account/food/ratings/$', api_views.UserRatings.as_view(), name='api-v1_1-user-rating'),
    url(r'^account/food/images/$', api_views.UserImages.as_view(), name='api-v1_1-user-image'),
    url(r'^account/food/comments/$', api_views.UserComments.as_view(), name='api-v1_1-user-comment'),
]
