from pymongo import MongoClient
from . import app

db = MongoClient(app.config['MONGO_URI'])[app.config['MONGO_DB']]