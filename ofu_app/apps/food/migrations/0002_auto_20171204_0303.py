# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 02:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='singlefood',
            name='image',
        ),
        migrations.AddField(
            model_name='singlefood',
            name='image',
            field=models.ManyToManyField(related_name='user_images', to='food.UserFoodImage'),
        ),
    ]
