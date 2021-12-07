import json

import pandas as pd
import pymongo

from run import all_events
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

def clipping():
    list_of_players = retriever.list_player_data()
    playerDict = get_player_match_events(list_of_players)
    playerDF = get_player_match_events_csv(playerDict)
    clipsdf = get_timelime_df(playerDF)
    events_json = all_events(clipsdf)
    data = pd.DataFrame(json.loads(events_json))
    normalized = to_formatted_json(data)

    for i in range(len(playerDF.index)):
        saver.update_player(list_of_players[i].get('_id'),normalized[i])
    return

def per_game(seasonId,playerName):
    list_of_players = retriever.list_player_data()
    playerDict = get_player_match_events(list_of_players)
    playerDf = get_player_match_events_csv(playerDict)
    stats = get_player_per_game(playerDf,playerName)
    normalized = to_formatted_json(stats)
    print(normalized)

    for i in range(len(playerDf.index)):
        saver.update_player(list_of_players[i].get('_id'),normalized[i])
    return
    #print(normalized)

if __name__== "__main__":
    #clipping()
    per_game("1","6113e3deb5ef4d0017b81701")
