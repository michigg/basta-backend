# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "home.jinja", {})


def links(request):
    return render(request, "links/home.jinja", {})


def impressum(request):
    return render(request, "impressum.jinja", {})
