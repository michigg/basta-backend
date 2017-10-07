import datetime

from django.shortcuts import render

from apps.events.models import Event


# Create your views here.
def events_main_page(request):
    return render(request, "events/home.jinja")


def all_events(request):
    today = datetime.datetime.now()
    all_future_events = Event.objects.filter(date__gte=today)
    lastdate = Event.objects.latest('date').date
    return render(request, "events/all_events.jinja", {
        'startdate': today,
        'events': all_future_events,
        'enddate': lastdate,
    })


def week_events(request):
    today = datetime.datetime.now()
    weekdelta = today + datetime.timedelta(7)
    events = Event.objects.filter(date__gte=today, date__lte=weekdelta)
    return render(request, "events/week_events.jinja", {
        'startdate': today,
        'enddate': weekdelta,
        'events': events,
    })
