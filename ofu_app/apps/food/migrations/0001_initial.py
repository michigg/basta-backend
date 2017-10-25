# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 21:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergene',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HappyHour',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('starttime', models.TimeField(default=django.utils.timezone.now)),
                ('endtime', models.TimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='SingleFood',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('price_student', models.CharField(max_length=10)),
                ('price_employee', models.CharField(max_length=10)),
                ('price_guest', models.CharField(max_length=10)),
                ('image', models.ImageField(blank=True, upload_to='food/%Y/%m/')),
                ('rating', models.FloatField(default=0)),
                ('first_star', models.SmallIntegerField(default=0)),
                ('second_star', models.SmallIntegerField(default=0)),
                ('third_star', models.SmallIntegerField(default=0)),
                ('fourth_star', models.SmallIntegerField(default=0)),
                ('fifth_star', models.SmallIntegerField(default=0)),
                ('allergens', models.ManyToManyField(to='food.Allergene')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='menu',
            field=models.ManyToManyField(to='food.SingleFood'),
        ),
        migrations.AlterUniqueTogether(
            name='happyhour',
            unique_together=set([('date', 'location', 'starttime', 'endtime')]),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('date', 'location')]),
        ),
    ]
