from django.shortcuts import render, redirect
from django.db.models import Min
from apps.donar.models import Room, Lecture, Lecture_Terms
from apps.donar.models import VGN_Coords


# Create your views here.
def home(request):
    return render(request, 'donar/home.jinja', {})


def all_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'donar/all_rooms.jinja', {'rooms': rooms})


def search_room(request):
    token = request.GET.get('search_room', None)
    if token:
        # create a form instance and populate it with data from the request:
        rooms_by_id = Room.objects.filter(short__contains=token)
        lectures = Lecture.objects.annotate(min_starttime=Min('term__starttime')).filter(name__contains=token).order_by('min_starttime')
        return render(request, 'donar/search_rooms.jinja', {'id': token, 'rooms': rooms_by_id, 'lectures': lectures})

    return render(request, 'donar/search_rooms.jinja', {})


def show_room(request, room):
    room = Room.objects.get(short=room)
    return render(request, 'donar/show_room.jinja', {'room': room})


def bus_connections(request):
    locations = VGN_Coords.objects.all()
    return render(request, 'donar/vgn_connections.jinja', {'locations': locations})


def vgn_redirect(request, position, vgn_coords):
    return redirect('https://www.vgn.de/verbindungen/?to=' + position + '&td=' + vgn_coords)
