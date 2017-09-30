# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_auto_20170929_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='happyhour',
            name='endtime',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='happyhour',
            name='starttime',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
