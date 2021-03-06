# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-24 08:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetabledata', '0009_auto_20180624_0733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='Data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetabledata.Data'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='code',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
