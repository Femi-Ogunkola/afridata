import json

import pandas as pd


def  get_player_match_events(eventList):
    playerMatchEventsDict = [event.get('playerMatchEvents') for event in eventList]
    return playerMatchEventsDict

def get_player_match_events_csv(file):
    data = pd.DataFrame(file)
    data = pd.json_normalize(data[0])
    return data

def get_timelime(data):
    clip = data.filter(regex='timeline')
    return clip.to_dict()

def get_timelime_df(data) -> pd.DataFrame:
    clip = data.filter(regex='timeline')
    a = pd.DataFrame.from_dict(clip)
    return a



def get_player_per_game(players: pd.DataFrame, player):
    A = players.loc[players['player_id'] == player ]
    players = players.select_dtypes(exclude=['object'])
    for i in players.columns:
       A[f"{i}/per_game"] = int(A[i].sum())/int(A['match'].nunique())
    return A

def total(players ,player):
    A = players.loc[players['player_id'] == player ]
    stat = {}
    for i in players.columns[8:]:
        stat[f"{i}"] = A[i].sum()

    return stat
    