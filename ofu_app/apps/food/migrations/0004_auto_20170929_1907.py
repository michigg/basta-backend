# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_auto_20170929_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='happyhour',
            name='endtime',
            field=models.DateField(default=datetime.datetime(2017, 9, 29, 19, 7, 24, 668322, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='happyhour',
            name='starttime',
            field=models.DateField(default=datetime.datetime(2017, 9, 29, 19, 7, 24, 668291, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='singlefood',
            name='name',
            field=models.CharField(unique=True, max_length=60),
        ),
        migrations.AlterUniqueTogether(
            name='happyhour',
            unique_together=set([('date', 'location')]),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('date', 'location')]),
        ),
    ]
