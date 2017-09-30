from django.shortcuts import render
from events.models import Event
import datetime


# Create your views here.
def week_events(request):
    today = datetime.datetime.now()
    weekdelta = today + datetime.timedelta(7)
    events = Event.objects.filter(date__gte=today, date__lte=weekdelta)
    return render(request, "events/week_events.jinja", {
        'startdate': today,
        'enddate': weekdelta,
        'events': events,
    })
