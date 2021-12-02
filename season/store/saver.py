# Python code to illustrate
# inserting data in MongoDB
from typing import Dict
from pymongo import MongoClient
from pymongo import database


class Saver:

    def __init__(self, database:database, dbName: str,collection: str):  
        self.dbName = database.afriskaut
        self.col = self.dbName.player

    def insert_one(self, playerJson: Dict):
        self.col.insert_one(playerJson)
