# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 01:44
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
                ('link', models.CharField(blank=True, max_length=60)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('presenter', models.CharField(blank=True, max_length=60)),
                ('orgname', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(blank=True, max_length=60)),
                ('name', models.CharField(max_length=60, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='locations',
            field=models.ManyToManyField(to='events.Location'),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('date', 'time', 'title')]),
        ),
    ]
