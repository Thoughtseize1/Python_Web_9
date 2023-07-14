import json
from bson.objectid import ObjectId
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from quotes.get_db import get_mongodb, get_local_mongodb, print_pidor


script_dir = os.path.dirname(os.path.abspath(__file__))
quotes_file_path = os.path.join(script_dir, "quotes.json")

with open(quotes_file_path, "r", encoding="utf-8") as file_with_quotes:
    quotes = json.load(file_with_quotes)


def load_in_cloud_db():
    db = get_mongodb()
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


def load_in_local_db():
    db = get_local_mongodb()
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


if __name__ == "__main__":
    load_in_local_db()

# Send a ping to confirm a successful connection
# try:
#     client.admin.command("ping")
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
