import json

import pandas as pd
import pymongo

from season.get_player_events import get_player_match_events, get_player_per_game
from season.get_player_events import get_player_match_events_csv
from season.get_player_events import get_timelime
from season.get_player_events import get_timelime_df
from season.store.normalize import to_formatted_json
from season.store.retriever import Retriever
from season.store.saver import Saver

client = pymongo.MongoClient("mongodb+srv://obafemi:obafemi@cluster0.kawbt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
retriever = Retriever(database=client, dbName='afriskaut', collection='player')
saver = Saver(database=client, dbName='afriskaut', collection='player')

def per_game(seasonId,playerName):
    per_game_saver = Saver(database=client, dbName='afriskaut', collection='per_game')
    list_of_players = retriever.list_player_data_season(seasonId)
    playerDict = get_player_match_events(list_of_players)
    playerDf = get_player_match_events_csv(playerDict)
    stats = get_player_per_game(playerDf,playerName)
    normalized = to_formatted_json(stats)
    per_game_events = []
    for j in range(len(normalized)):
        for i in range(len(list_of_players)):
            if list_of_players[i].get('playerMatchEvents')[0].get('player_id') == playerName :
                list_of_players[i].get('playerMatchEvents')[0] = normalized[j]
                per_game_events.append(list_of_players[i])
    saver.insert_per_game(per_game_events)
    return

if __name__== "__main__":
    #clipping()
    per_game(1,"6113e3deb5ef4d0017b81715")
