import pymongo
import json
from season.store.retriever import Retriever
from season.store.saver import Saver

client = pymongo.MongoClient("mongodb+srv://obafemi:obafemi@cluster0.kawbt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
retriever = Retriever(database=client, dbName='afriskaut', collection='player')
saver = Saver(database=client, dbName='afriskaut', collection='player')

#with open('player.json') as f:
#    playerJson = json.loads(f.read())
#print(type(playerJson))
#saver.insert_one(playerJson=playerJson)
#retriever.list_player_data()