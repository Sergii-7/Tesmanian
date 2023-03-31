from bson import ObjectId
from pymongo import MongoClient
import config

client = MongoClient(
    f"mongodb+srv://{config.mongo_name}:{config.mongo_pass}@cluster0.yhicgc7.mongodb.net/?retryWrites=true&w=majority"
)
db = client.Tesmanian

if db != None:
    print('MongoDB Tesmanian connected! 👍👌')
