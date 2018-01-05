# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-21 11:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('price_student', models.CharField(blank=True, max_length=10, null=True)),
                ('price_employee', models.CharField(blank=True, max_length=10, null=True)),
                ('price_guest', models.CharField(blank=True, max_length=10, null=True)),
                ('rating', models.FloatField(default=0)),
                ('allergens', models.ManyToManyField(blank=True, to='food.Allergene')),
            ],
        ),
        migrations.CreateModel(
            name='UserFoodImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='food/originals/%Y/%m/%W')),
                ('thumbnail', models.ImageField(blank=True, upload_to='food/thumbs/%Y/%m/%W')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.SingleFood')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.FloatField(default=0)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.SingleFood')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='singlefood',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='food.UserFoodImage'),
        ),
        migrations.AddField(
            model_name='menu',
            name='menu',
            field=models.ManyToManyField(related_name='foods', to='food.SingleFood'),
        ),
        migrations.AlterUniqueTogether(
            name='happyhour',
            unique_together=set([('date', 'location', 'starttime', 'endtime')]),
        ),
        migrations.AlterUniqueTogether(
            name='userfoodimage',
            unique_together=set([('user', 'food')]),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('date', 'location')]),
        ),
    ]
