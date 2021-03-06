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

from apps.donar import views

urlpatterns = [
    url(r'^$', views.home, name='donar'),
    url(r'^all$', views.all_rooms, name='all-rooms'),
    url(r'^search/$', views.search_room, name='search-rooms'),
    url(r'^search/(?P<room>.+/.+)/$', views.show_room, name='show-room'),
    url(r'^search/(?P<room>.+)/$', views.show_room, name='show-room'),

    # VGN
    url(r'^bus/$', views.bus_connections, name='vgn-bus'),
    url(r'^bus/(?P<vgn_coords>.+)/(?P<position>.+)/$', views.vgn_redirect, name='vgn-redirect'),
]
