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
from django.urls import path
from apps.food.api.v1_2.views import main_views as api_views
from apps.food.api.v1_2.views import user_views as user_api_views

urlpatterns = [
    # API Version 1.2
    path('food/menus/', api_views.ApiMenus.as_view(), name='menus'),
    path('food/menus/<int:pk>/', api_views.ApiMenu.as_view(), name='menu'),
    path('food/menus/locations', api_views.ApiMenusLocations.as_view(), name='menus-locations'),

    path('food/meals/', api_views.ApiMeals.as_view(), name='meals'),
    path('food/meals/<int:pk>', api_views.ApiMeal.as_view(), name='meal'),
    path('food/meals/<int:pk>/comments', api_views.ApiMealComments.as_view(), name='meal-comments'),

    path('food/meals/<int:pk>/comment', user_api_views.ApiUserFoodCommentUpload.as_view(), name='meals-comment-upload'),
    path('food/meals/<int:pk>/rating', user_api_views.ApiFoodRatingUpload.as_view(), name='meals-rating-upload'),
    path('food/meals/<int:pk>/image', user_api_views.ApiFoodImageUpload.as_view(), name='meals-image-upload'),
    path('food/meals/image', user_api_views.ApiFoodImageUpload.as_view(), name='meals-image-upload'),

    path('food/meals/images/', api_views.ApiFoodImages.as_view(), name='images'),
    path('food/meals/images/default', api_views.ApiFoodImagesDefault.as_view(), name='images-default'),

    path('food/allergens/', api_views.ApiAllergens.as_view(), name='allergens'),

    path('food/happy-hours/', api_views.ApiHappyHours.as_view(), name='happy-hours'),
    path('food/happy-hours/<int:pk>', api_views.ApiHappyHours.as_view(), name='happy-hours'),
    path('food/happy-hours/locations', api_views.ApiHappyHoursLocations.as_view(), name='happy-hours-locations'),
]
