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
from apps.bug_report.api.v1_2 import views as api_views

urlpatterns = [
    # API Version 1.2
    path('bug-report/reports/', api_views.ApiBugMsgs.as_view(), name='bug-reports'),
    path('bug-report/reports/<int:pk>/', api_views.ApiBugMsgUpdate.as_view(), name='bug-report'),
    path('bug-report/priorities/', api_views.ApiBugPriorities.as_view(), name='bug-priorities'),
    path('bug-report/categories/', api_views.ApiBugCategories.as_view(), name='bug-categories'),
    path('bug-report/states/', api_views.ApiBugStates.as_view(), name='bug-states'),
]
