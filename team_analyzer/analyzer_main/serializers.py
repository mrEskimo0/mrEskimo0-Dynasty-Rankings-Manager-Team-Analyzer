from rest_framework import serializers
from .models import *

class Player_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class Ranking_Serializer(serializers.ModelSerializer):
    player = Player_Serializer(read_only=True)
    class Meta:
        model = Ranking
        fields = ['player','value','date_last_updated']
