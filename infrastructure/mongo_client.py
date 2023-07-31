import os

from app.domain.model import mongo as db
from pymongo import MongoClient
from typing import Type

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'root')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'example')
DB_NAME = os.environ.get('MONGO_DBNAME', 'mydatabase')


def get_mongo(collection: Type[db.AbstractCollection]):
    client = MongoClient(
        MONGO_URI,
        # username=MONGO_USERNAME,
        # password=MONGO_PASSWORD,
        # authSource="admin",
    )
    database = client[DB_NAME]
    return database[collection.__collection_name__]
