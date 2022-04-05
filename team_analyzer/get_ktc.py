import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from os import path

#get trade values from KTC website
#can optionally specify superflex/non-SF (sf by default)
#can optionally include draft pick values (included by default)
def getTradeValues(superflex=True, include_picks=True):
    url = 'https://keeptradecut.com/dynasty-rankings?filters=QB|WR|RB|TE'
    if include_picks:
        url = url + '|RDP'
    if not superflex:
        url = url + '&format=1'
    players = BeautifulSoup(get(url).text, features='lxml').select('div[id=rankings-page-rankings] > div')
    player_list = []
    for player in players:
        e = player.select('div[class=player-name] > p > a')[0]
        pid = e.get('href').split('/')[-1]
        name = e.text.strip()
        try:
            team = player.select('div[class=player-name] > p > span[class=player-team]')[0].text.strip()
        except:
            team = None
        position = player.select('p[class=position]')[0].text.strip()[:2]
        position = 'PICK' if position == 'PI' else position
        try:
            age = player.select('div[class=position-team] > p')[1].text.strip()[:2]
        except:
            age = None
        val = int(player.select('div[class=value]')[0].text.strip())

        val_colname = 'SF Value' if superflex else 'Non-SF Value'

        val_colname = 'SF_Value' if superflex else 'Non_SF_Value'

        player_list.append({'PlayerID':pid,'Name':name,'Team':team,'Position':position,'Age':age,val_colname:val})
    return pd.DataFrame(player_list)

#combine dataframes with superflex/non-sf values into single dataframe
def combineTradeValues(sf_df, nonsf_df):
    merged_df = pd.merge(sf_df, nonsf_df, how='outer', on='PlayerID', suffixes=('_sf','_nonsf'))
    for col in ['Name','Team','Position','Age']:
        merged_df[col] = merged_df[col + '_sf'].fillna(merged_df[col + '_nonsf'])

    return merged_df[['PlayerID','Name','Team','Position','Age','SF_Value','Non_SF_Value']]
