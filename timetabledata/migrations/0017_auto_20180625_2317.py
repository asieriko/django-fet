# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-25 23:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetabledata', '0016_auto_20180625_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='Data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetabledata.Data'),
        ),
        migrations.RemoveField(
            model_name='data',
            name='Room',
        ),
        migrations.AddField(
            model_name='data',
            name='Room',
            field=models.ManyToManyField(blank=True, null=True, to='timetabledata.Room'),
        ),
    ]