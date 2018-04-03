# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from apps.food.models import SingleFood, Menu, HappyHour, UserFoodRating, UserFoodImage, FoodImage, UserFoodComment


class SingleFoodInline(admin.TabularInline):
    model = Menu.menu.through
    extra = 1
    # fields = ['menu__image', ]


class MenuAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    inlines = [
        SingleFoodInline,
    ]
    exclude = ('menu',)


# Register your models here.
admin.site.register(SingleFood)
admin.site.register(HappyHour)
admin.site.register(UserFoodRating)
admin.site.register(UserFoodImage)
admin.site.register(UserFoodComment)
admin.site.register(Menu, MenuAdmin)
admin.site.register(FoodImage)
