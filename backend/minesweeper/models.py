# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Board(models.Model):
    game_code = models.TextField(default="")
    game_state = models.TextField(default="")
    game_rows = models.IntegerField(default=9)
    game_columns = models.IntegerField(default=9)
    game_num_of_bombs = models.IntegerField(default=10)
    game_guiString = models.TextField(default="")


