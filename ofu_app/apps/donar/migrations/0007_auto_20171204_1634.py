# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 15:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('donar', '0006_auto_20171204_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture_terms',
            name='starttime',
            field=models.TimeField(default=datetime.datetime(2017, 12, 4, 15, 34, 41, 765204, tzinfo=utc)),
        ),
    ]
