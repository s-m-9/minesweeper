from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "game_code", "game_state", "game_rows", "game_columns", "game_num_of_bombs", "game_guiString"] 
