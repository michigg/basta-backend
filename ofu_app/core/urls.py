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
from core import views
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework import routers
from apps.food import urls as food_urls
from django.conf import settings
from django.conf.urls.static import static

# API router
api_router_v1 = routers.DefaultRouter()
api_router_v1.registry.extend(food_urls.apiRouter_v1.registry)

api_router_v1_1 = routers.DefaultRouter()
api_router_v1_1.registry.extend(food_urls.apiRouter_v1_1.registry)

urlpatterns = [
                  url(r'^login/$', auth_views.login, {'template_name': 'registration/login.jinja'}, name='login'),
                  url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
                  url(r'^admin/', admin.site.urls),
                  # url(r'^signup/$', core_views.signup, name='signup'),
                  url(r'^account/', include("apps.registration.urls")),

                  url(r'^$', views.home, name="home"),

                  # -- Apps --
                  url(r'^food/', include('apps.food.urls')),
                  url(r'^events/', include('apps.events.urls')),
                  url(r'^donar/', include('apps.donar.urls')),
                  url(r'^links/$', views.links, name='links-home'),
                  url(r'^impressum/$', views.impressum, name='impressum'),

                  # -- API --
                  url(r'^api/v1/', include(api_router_v1.urls)),
                  url(r'^api/v1.1/', include(api_router_v1_1.urls)),
                  url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
