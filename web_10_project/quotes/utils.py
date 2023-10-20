from pymongo import MongoClient


def get_mongodb():
    client = MongoClient("mongodb://localhost")

    db = client.web_10
    return db
