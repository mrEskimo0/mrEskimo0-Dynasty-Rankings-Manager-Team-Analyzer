import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_analyzer.settings')

import django
django.setup()

#put population script here
from analyzer_main.models import Player
from django.db import IntegrityError
import pandas as pd
import json
import json
import requests

def get_data():
    solditems = requests.get('https://api.sleeper.app/v1/players/nfl') # (your url)
    data = solditems.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)

#player = Player.objects.get_or_create(name=var,id=var,...)

def populate_players():
    path_to_json = "data.json"

    with open(path_to_json, "r") as read_file:
        data = json.load(read_file)

    players_df = pd.DataFrame.from_dict(data, orient='index')

    players_df_cleaned = players_df.filter(['player_id','full_name','fantasy_positions'])

    pos = ['QB','RB','WR','TE']
    fantasy_only = players_df_cleaned[players_df_cleaned.applymap(lambda x: x[0] if isinstance(x, list) else x)['fantasy_positions'].isin(pos)]

    for row in fantasy_only.itertuples():
        p_name = row.full_name
        p_id = row.player_id
        p_position = row.fantasy_positions[0]

        try:
            player = Player.objects.get_or_create(name=p_name,id=p_id,position=p_position)[0]
        except IntegrityError:
            Player.objects.get(id=p_id).delete()
            if p_name == 'Player Invalid':
                continue
            else:
                Player.objects.create(name=p_name,id=p_id,position=p_position)

def populate_picks():
    for i in range(2022, 2025):
        for j in range(1, 61):
            p_name = str(i) + ' Pick ' + str(j)
            p_position = 'Pick'
            p_id = str(i)+'-'+str(j)
            player = Player.objects.get_or_create(name=p_name,id=p_id,position=p_position)[0]

if __name__ == '__main__':
    get_data()
    populate_players()
    populate_picks()
