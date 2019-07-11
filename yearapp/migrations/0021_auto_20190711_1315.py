# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-11 13:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yearapp', '0020_auto_20190711_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='class_of_the_year',
        ),
        migrations.AddField(
            model_name='project',
            name='Class_year',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
