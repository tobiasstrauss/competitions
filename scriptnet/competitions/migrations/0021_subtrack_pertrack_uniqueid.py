# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0020_track_percomp_uniqueid'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtrack',
            name='pertrack_uniqueid',
            field=models.IntegerField(default='1'),
        ),
    ]