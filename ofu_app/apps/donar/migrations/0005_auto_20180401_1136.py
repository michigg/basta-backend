# Generated by Django 2.0.1 on 2018-04-01 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donar', '0004_auto_20180117_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='short',
            field=models.CharField(max_length=256),
        ),
    ]
