# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-07 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20180413_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(upload_to='static/image/', verbose_name='img'),
        ),
    ]
