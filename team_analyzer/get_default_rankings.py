import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_analyzer.settings')

import django
django.setup()

import csv
from analyzer_main.models import *
import pandas as pd
import numpy as np
import datetime
from django.db.models import Q
from get_ktc import getTradeValues, combineTradeValues


def new_adjust_vals(val):
    new_scale = [.75,.825,.95,1.1,1.1,1,1.6,1.1,3.8,1.8,1.6,1.4,1.5,1.8,2.5,2.5,2.5,2.55,2.8,3.5]

    loops = int(val//500)
    remainder = val%500

    multiplied = 0
    last_scale = 0

    for x, i in enumerate(range(loops)):
        multiplied += 500*new_scale[x]
        last_scale = x

    multiplied += remainder*new_scale[last_scale+1]
    multiplied = round(multiplied,1)
    return multiplied

def run_the_scrape():

    sf_df = getTradeValues(superflex=True)
    nonsf_df = getTradeValues(superflex=False)

    sf_df['SF_Value'] = sf_df['SF_Value'].apply(new_adjust_vals)
    nonsf_df['Non_SF_Value'] = nonsf_df['Non_SF_Value'].apply(new_adjust_vals)

    merged_df = combineTradeValues(sf_df, nonsf_df)

    #need to split merged_df into 1 df of picks and another of just players
    picks_df = merged_df[merged_df['Position'] == 'PICK']
    merged_df = merged_df[merged_df['Position'] != 'PICK']

    #get the years of picks that are ranked
    group_df = picks_df.copy()
    group_df['Year'] = group_df['Name'].apply(lambda val: val[0:4])
    grouped = group_df.groupby(['Year'])

    #group picks by year, make a df for every years' picks
    pick_dfs = []
    for year in grouped.groups.keys():
        year_df = picks_df.loc[picks_df['Name'].str.contains(str(year))]
        pick_dfs.append(year_df)
        #use a .loc to make a new df for every year in the ktc .ranks

    #if the newest picks arent in ktc ranks, copy latest year's picks and change the year in name to latest + 1
    if len(pick_dfs) <= 3:
        year_df = pick_dfs[len(pick_dfs)-1].copy()
        year_df['Name'] = year_df['Name'].apply(lambda val: str(int(val[0:4])+1) + val[4:])
        year_df['PlayerID'] = year_df['PlayerID'].apply(lambda val: str(int(val[0:4])+1) + val[4:])
        pick_dfs.append(year_df)

    def_user = User.objects.get(username='mrEskimo0')
    u_ranking = User_Ranking.objects.get(name='Consensus Superflex')
    u_ranking_standard = User_Ranking.objects.get(name='Consensus Standard')
    date_today = datetime.date.today().strftime('%Y-%m-%d')

    picks_map(pick_dfs, def_user, u_ranking, u_ranking_standard, date_today)

    for player in merged_df.itertuples():
        player_name = player.Name
        replaced_name = player.Name.replace('.','')
        bad_names = {'Kenneth Walker III':'Kenneth Walker', 'Irv Smith Jr.':'Irv Smith', 'Will Fuller':'William Fuller', 'Calvin Austin III':'Calvin Austin','Jeffery Wilson':'Jeff Wilson','Pierre Strong Jr.':'Pierre Strong','Olabisi Johnson':'Bisi Johnson','Lamical Perine':'La\'Mical Perine','Josh Palmer':'Joshua Palmer','LJ Scott':'L.J. Scott','DK Metcalf':'D.K. Metcalf'}
        if player_name in bad_names.keys():
            player_name = bad_names[player_name]
        if Player.objects.filter(name=player_name).exists() or Player.objects.filter(name=replaced_name).exists():
            if Player.objects.filter(name=player_name).exists():
                #regular name passed and is fine
                pass
            else:
                #dots in name need to be replaced to map
                player_name = replaced_name

            db_players = Player.objects.filter(name=player_name)
            db_players = db_players.filter(Q(position='QB') | Q(position='RB') | Q(position='WR') | Q(position='TE'))

            for db_player in db_players:
                #create superflex
                sf_object, created_sf = Ranking.objects.update_or_create(
                    user_ranking=u_ranking,
                    user=def_user,
                    player=db_player,
                    defaults={'value':player.SF_Value, 'date_last_updated':date_today}
                )

                standard_object, created_non = Ranking.objects.update_or_create(
                    user_ranking=u_ranking_standard,
                    user=def_user,
                    player=db_player,
                    defaults={'value':player.Non_SF_Value, 'date_last_updated':date_today}
                )

                try:
                    Ranking_History.objects.get_or_create(ranking=sf_object, date=date_today)
                    Ranking_History.objects.get_or_create(ranking=standard_object, date=date_today)
                except sf_object.DoesNotExist:
                    Ranking_History.objects.get_or_create(ranking=created_sf, date=date_today)
                    Ranking_History.objects.get_or_create(ranking=created_non, date=date_today)

        else:
            print(player_name + ' and '+replaced_name+' dont match')


def picks_map(list_of_dfs, def_user, u_ranking, u_ranking_standard, date_today):

    early_first = [1.33,1.13,.985,.945]
    early = [1.065,1.03,.985,.945]
    mid = [1.02,.985,.96,.945]
    late = [1.05,1.015,.96,.935]

    for df in list_of_dfs:
        year = df.iloc[0]['Name'][0:4]
        for num, pick in enumerate(df.itertuples()):
            if num == 0:
                #Early 1st, use early_first
                picks = num + 4
                for i in range(picks):
                    pick_id = year+'-'+str(i+1)
                    pick_obj = Player.objects.get(id=pick_id)
                    pick_val_sf = round(pick.SF_Value*early_first[i],1)
                    pick_val_non = round(pick.Non_SF_Value*early_first[i],1)

                    pick_rank_obj, created_sf = Ranking.objects.update_or_create(
                        user_ranking=u_ranking,
                        user=def_user,
                        player=pick_obj,
                        defaults={'value':pick_val_sf, 'date_last_updated':date_today}
                    )

                    pick_rank_obj_non, created_non = Ranking.objects.update_or_create(
                        user_ranking=u_ranking_standard,
                        user=def_user,
                        player=pick_obj,
                        defaults={'value':pick_val_non, 'date_last_updated':date_today}
                    )

                    try:
                        Ranking_History.objects.get_or_create(ranking=pick_rank_obj, date=date_today)
                        Ranking_History.objects.get_or_create(ranking=pick_rank_obj_non, date=date_today)
                    except UnboundLocalError:
                        Ranking_History.objects.get_or_create(ranking=created_sf, date=date_today)
                        Ranking_History.objects.get_or_create(ranking=created_non, date=date_today)

            else:
                picks = (num*4)+1
                #look for early mid or late
                for x, i in enumerate(range(picks,picks+4)):

                    #this needs to be multiplied by num
                    pick_id = year+'-'+str((num*4)+x+1)
                    print(pick_id)
                    pick_obj = Player.objects.get(id=pick_id)

                    #need to lookup which list we are using
                    if 'Early' in pick.Name:
                        pick_val_sf = round(pick.SF_Value*early[x],1)
                        pick_val_non = round(pick.Non_SF_Value*early[x],1)

                    elif 'Mid' in pick.Name:
                        pick_val_sf = round(pick.SF_Value*mid[x],1)
                        pick_val_non = round(pick.Non_SF_Value*mid[x],1)

                    elif 'Late' in pick.Name:
                        pick_val_sf = round(pick.SF_Value*late[x],1)
                        pick_val_non = round(pick.Non_SF_Value*late[x],1)

                    pick_rank_obj, created_sf = Ranking.objects.update_or_create(
                        user_ranking=u_ranking,
                        user=def_user,
                        player=pick_obj,
                        defaults={'value':pick_val_sf, 'date_last_updated':date_today}
                    )

                    pick_rank_obj_non, created_non = Ranking.objects.update_or_create(
                        user_ranking=u_ranking_standard,
                        user=def_user,
                        player=pick_obj,
                        defaults={'value':pick_val_non, 'date_last_updated':date_today}
                    )

                    try:
                        Ranking_History.objects.get_or_create(ranking=pick_rank_obj, date=date_today)
                        Ranking_History.objects.get_or_create(ranking=pick_rank_obj_non, date=date_today)
                    except (pick_rank_obj.DoesNotExist, pick_rank_obj_non.DoesNotExist, UnboundLocalError) as e:
                        Ranking_History.objects.get_or_create(ranking=created_sf, date=date_today)
                        Ranking_History.objects.get_or_create(ranking=created_non, date=date_today)

# run_the_scrape()
