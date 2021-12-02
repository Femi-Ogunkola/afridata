# Python code to illustrate
# inserting data in MongoDB
from typing import Dict
from pymongo import MongoClient
from pymongo import database


class Saver:

    def __init__(self,database:database, dbName: str,collection: str):  
        self.dbName = database[dbName]
        self.col = dbName[collection]

    def insert_one(self, playerJson: Dict):
        self.col.insert_one( playerJson) 
        




#try:
#	conn = MongoClient("mongodb+srv://obafemi:obafemi@cluster0.kawbt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#	print("Connected successfully!!!")
#except:
#	print("Could not connect to MongoDB")

# database
#db = conn.afriskaut

# Created or Switched to collection names: my_gfg_collection
#collection = db.player
'''emp_rec1 = {
		"name":"Mr.Geek",
		"eid":24,
		"location":"delhi"
		}
emp_rec2 = {
		"name":"Mr.Shaurya",
		"eid":14,
		"location":"delhi"
		}
# Insert Data
rec_id1 = collection.insert_one(emp_rec1)
rec_id2 = collection.insert_one(emp_rec2)

print("Data inserted with record ids",rec_id1," ",rec_id2)

# Printing the data inserted
cursor = collection.find()
for record in cursor:
	print(record)'''