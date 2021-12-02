from typing import List
from pymongo import database


class Retriever:

    def __init__(self,dbName: str,collection: str):  
        self.dbName = database[dbName]
        self.col = dbName[collection]

    def list_player_data(self) -> List:
        return self.col.find()

