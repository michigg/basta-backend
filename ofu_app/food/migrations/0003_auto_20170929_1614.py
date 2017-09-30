# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_auto_20170929_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='happyhour',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='happyhour',
            name='description',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='happyhour',
            name='location',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='menu',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='menu',
            name='location',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='singlefood',
            name='name',
            field=models.CharField(max_length=60),
        ),
    ]
