from rest_framework import serializers
from analyzer_main.models import *

class League_Table_Serializer(serializers.ModelSerializer):
    class Meta:
        model = table_league_total
        fields = '__all__'

class League_Output_Serializer(serializers.ModelSerializer):
    class Meta:
        model = league_output
        fields = '__all__'

class Total_Value_Serializer(serializers.ModelSerializer):
    class Meta:
        model = league_output
        fields = ['display_name', 'value']

class Position_Serializer(serializers.ModelSerializer):
    class Meta:
        model = league_output
        fields = ['position', 'value']
