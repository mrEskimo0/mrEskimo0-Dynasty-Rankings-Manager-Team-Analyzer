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

# class Team_Serializer(serializers.ModelSerializer):
#     players = Ranking_Serializer(many=True, read_only=True)
#
#     class Meta:
#         model = Team
#         fields = ['team','team_name','user_ranking','players']

    # def get_rankings(self, Team):
        # return Ranking_Serializer(many=True)

    # def create(self, player_ids):
    #     ids = player_ids.pop('')

# class Team_Serializer(serializers.Serializer):
#     team_name = serializers.CharField(max_length=100)
#     players = Ranking_Serializer(many=True)
#     total_value = serializers.FloatField()


# class Team_Serializer(serializers.Serializer):
#     team_name = charfield, got from data in sleeper json output that i put into pandas df
#     players = another serializer, only want players with our id or team name
#     total_value = is calculated by summing all the players

# class League_Serializer(serializers.ModelSerializer):
#     teams = Team_Serializer(many=True)
#
#     class Meta:
#         model = League
#         fields = ['name', 'teams']

# class new_Player_Serializer(serializers.ModelSerializer):
#     value =
#     display_name =
#     class Meta:
#         model = Player
#         fields = '__all__'
