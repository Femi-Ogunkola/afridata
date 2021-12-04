import pymongo
import json
from season.get_player_events import get_player_match_events, get_player_match_events_csv
from season.store.retriever import Retriever
from season.store.saver import Saver

client = pymongo.MongoClient("mongodb+srv://obafemi:obafemi@cluster0.kawbt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
retriever = Retriever(database=client, dbName='afriskaut', collection='player')
saver = Saver(database=client, dbName='afriskaut', collection='player')

list_of_players = retriever.list_player_data()
playerDict = get_player_match_events(list_of_players)
playerDF = get_player_match_events_csv(playerDict)

