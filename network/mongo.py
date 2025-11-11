import os
from pymongo import MongoClient

# 環境変数 MONGO_URI を使う
# 例: mongodb://appUser:StrongAppPass123!@10.0.2.123:27017/?authSource=assignment8
def get_collection():
    uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
    client = MongoClient(uri, serverSelectionTimeoutMS=2000)
    db = client['assignment8']
    return db['leases']