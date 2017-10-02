# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-02 20:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=60)),
                ('category', models.CharField(max_length=60)),
                ('link', models.CharField(max_length=60)),
                ('location', models.CharField(max_length=60)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('date', 'location')]),
        ),
    ]
