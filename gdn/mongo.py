from pymongo import MongoClient
from . import app

db = MongoClient(app.config['MONGO_URI'])[app.config['MONGO_DB']]

db.usage.ensure_index('last_request', expireAfterSeconds=app.config['KEEP_USAGE_FOR'])
db.usage.ensure_index('ip')

db.items.ensure_index('resource')
db.items.ensure_index('parents')