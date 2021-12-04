import pymongo
import json
import pandas as pd
from run import all_events
from season.get_player_events import get_player_match_events, get_player_match_events_csv, get_timelime, get_timelime_df
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


if __name__== "__main__":
    clipping()


