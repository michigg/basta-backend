import datetime
from time import time

from django.shortcuts import render

from apps.events.models import Event


# Helper Methods
def get_categories(events: list):
    categories = []
    for event in events:
        if not categories.__contains__(event.category):
            categories.append(event.category)
    return categories


# Create your views here.
def events_main_page(request):
    return render(request, "events/home.jinja")


def all_events(request):
    today = datetime.datetime.now()
    all_future_events = Event.objects.filter(date__gte=today).order_by('date', 'time')
    lastdate = Event.objects.latest('date').date
    return render(request, "events/all_events.jinja", {
        'startdate': today,
        'events': all_future_events,
        'enddate': lastdate,
        'categories': get_categories(all_future_events),
    })


def week_events(request):
    today = datetime.datetime.now()
    weekdelta = today + datetime.timedelta(7)
    events = Event.objects.filter(date__gte=today, date__lte=weekdelta).order_by('date', 'time')
    return render(request, "events/week_events.jinja", {
        'startdate': today,
        'enddate': weekdelta,
        'events': events,
        'categories': get_categories(events),
    })


def day_events(request):
    today = datetime.datetime.now()
    events = Event.objects.filter(date=today).order_by('time')
    return render(request, "events/day_events.jinja", {
        'date': today,
        'events': events,
        'categories': get_categories(events),
    })
