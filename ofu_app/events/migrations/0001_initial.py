# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
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
