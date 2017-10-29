from django.contrib import admin
from apps.donar.models import Room, Lecture, Lecture_Terms, VGN_Coords
# Register your models here.
admin.site.register(Room)
admin.site.register(Lecture)
admin.site.register(Lecture_Terms)
admin.site.register(VGN_Coords)