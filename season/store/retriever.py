from typing import List

from pymongo import database


class Retriever:
    def __init__(self,database, dbName: str,collection: str):  
        self.dbName = database[dbName]
        self.col = self.dbName[collection]

    def list_player_data(self) -> List:
        a =  [elem for elem in self.col.find()]
        return a

    def list_player_data_match(self,matchId):
        a = [elem for elem in self.col.find({playerMatchEvents: { match: matchId }})]
        return a

    def list_player_data_season(self, seasonId):
        a = [elem for elem in self.col.find( {season: seasonId })]
        return a
    
    def list_player_data_position(self, playerPosition):
        a = [elem for elem in self.col.find( {position: playerPosition })]
        return a
