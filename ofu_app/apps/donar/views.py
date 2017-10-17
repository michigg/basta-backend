from django.shortcuts import render

from apps.donar.models import Room
from apps.donar.models import VGN_Coords


# Create your views here.
def home(request):
    return render(request, 'donar/home.jinja', {})


def all_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'donar/all_rooms.jinja', {'rooms': rooms})


def search_room(request):
    id = request.GET.get('search_room', None)
    if id:
        # create a form instance and populate it with data from the request:
        rooms = Room.objects.filter(short__contains=id)
        return render(request, 'donar/search_rooms.jinja', {'id': id, 'rooms': rooms})

    return render(request, 'donar/search_rooms.jinja', {})


def show_room(request, room):
    room = Room.objects.get(short=room)
    return render(request, 'donar/show_room.jinja', {'room': room})


def bus_connections(request):
    locations = VGN_Coords.objects.all()
    return render(request, 'donar/vgn_connections.jinja', {'locations': locations})
