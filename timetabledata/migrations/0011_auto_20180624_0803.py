# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-24 08:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetabledata', '0010_auto_20180624_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='Data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetabledata.Data'),
        ),
        migrations.AlterField(
            model_name='data',
            name='Type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetabledata.ConexionType'),
        ),
    ]
