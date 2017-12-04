# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 14:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_auto_20171204_0454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='menu',
        ),
        migrations.AddField(
            model_name='menu',
            name='menu',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food.SingleFood'),
            preserve_default=False,
        ),
    ]
