# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-14 15:22
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_auto_20180514_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='desc',
            field=tinymce.models.HTMLField(default=''),
        ),
    ]
