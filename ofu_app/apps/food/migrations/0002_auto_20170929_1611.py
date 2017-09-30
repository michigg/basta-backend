# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='happyhour',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='singlefood',
            name='uuid',
        ),
        migrations.AlterField(
            model_name='happyhour',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='singlefood',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
