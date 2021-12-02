import pymongo
import season.store.retriever as Retriever

client = pymongo.MongoClient("mongodb+srv://obafemi:obafemi@cluster0.kawbt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
retriever = Retriever(database=client,dbName='afriksaut', collection='player')