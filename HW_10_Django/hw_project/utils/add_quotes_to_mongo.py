import json
import os
import sys

from bson.objectid import ObjectId
from pymongo import MongoClient

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from useful_quotes.utils import get_local_mongodb

script_dir = os.path.dirname(__file__)

client = MongoClient("mongodb://localhost")

quotes_file_path = os.path.join(script_dir, "quotes.json")
db = get_local_mongodb()

with open(quotes_file_path, "r", encoding="utf-8") as fd:
    quotes = json.load(fd)

for quote in quotes:
    author = db.authors.find_one({"fullname": quote["author"]})
    if author:
        db.quotes.insert_one(
            {
                "quote": quote["quote"],
                "tags": quote["tags"],
                "author": ObjectId(author["_id"]),
            }
        )
