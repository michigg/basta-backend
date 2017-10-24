# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-04 00:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donar', '0002_auto_20171004_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='room',
            name='size',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='room',
            name='address',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='room',
            name='building_key',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='room',
            name='floor',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='room',
            name='key',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='room',
            name='orgname',
            field=models.CharField(default='', max_length=60),
        ),
    ]
