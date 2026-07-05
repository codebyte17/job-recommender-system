from pymongo import MongoClient
from config import settings

_client = MongoClient(settings.mongo_uri)

db = _client[settings.mongo_db_name]