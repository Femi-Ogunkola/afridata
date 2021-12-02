from typing import List
from pymongo import database


class Retriever:
    def __init__(self,database, dbName: str,collection: str):  
        self.dbName = database[dbName]
        self.col = self.dbName[collection]

    def list_player_data(self) -> List:
        a =  [elem for elem in self.col.find()]
        return a

