# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 03:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('donar', '0003_auto_20171204_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture_terms',
            name='starttime',
            field=models.TimeField(default=datetime.datetime(2017, 12, 4, 3, 47, 55, 513852, tzinfo=utc)),
        ),
    ]
