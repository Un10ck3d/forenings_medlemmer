# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-08 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0079_auto_20161008_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, verbose_name='Længdegrad'),
        ),
        migrations.AlterField(
            model_name='department',
            name='longtitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, verbose_name='Breddegrad'),
        ),
    ]
