# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-11 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minesweeper', '0009_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='game_guiString',
            field=models.TextField(default=''),
        ),
    ]
