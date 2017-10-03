from django.shortcuts import render

from apps.donar.models import Room


# Create your views here.
def home(request):
    rooms = Room.objects.all()
    return render(request, 'donar/home.jinja', {'rooms': rooms})
