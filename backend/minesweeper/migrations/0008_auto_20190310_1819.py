# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-10 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minesweeper', '0007_auto_20190310_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='game_code',
            field=models.TextField(default=''),
        ),
    ]