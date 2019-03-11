# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Board

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    showBoard = ("game_code", "game_state", "game_rows", "game_columns", "game_num_of_bombs")


admin.site.register(Board, BoardAdmin)
