# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20161211_0151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='id',
        ),
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
