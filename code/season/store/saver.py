# Python code to illustrate
# inserting data in MongoDB
from typing import Dict
from typing import List

from pymongo import MongoClient
from pymongo import database


class Saver:

    def __init__(self, database:database, dbName: str,collection: str):  
        self.dbName = database.afriskaut
        self.col = self.dbName.player

    def insert_one(self, playerJson: Dict):
        self.col.insert_one(playerJson)
    
    def insert_per_game_one(self, playerJson: Dict):
        self.dbName.per_game.insert_one(playerJson)

    def insert(self, playerList: List):
        for i in range(len(playerList)):
            self.insert_one(playerList[i])

    def insert_per_game(self, playerList: List):
        for i in range(len(playerList)):
            self.insert_per_game_one(playerList[i])
    
    def update_player(self,playerId: str,updatedPlayerMatchEvents):
        myQuery = { "_id": playerId }   
        newvalues = { "$set": { "playerMatchEvents": updatedPlayerMatchEvents } }
        self.dbName.per_game.update_one(myQuery, newvalues)