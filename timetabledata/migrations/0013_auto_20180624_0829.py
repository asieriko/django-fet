# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-24 08:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetabledata', '0012_auto_20180624_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='Data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetabledata.Data'),
        ),
    ]
