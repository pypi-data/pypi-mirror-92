import os

from pymongo import MongoClient


def client(url=None):
    if url is None:
        url = os.environ.get('SEC__MONGO_URL')
    return MongoClient(url)
