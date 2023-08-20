import sqlite3
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import configparser
import os

from hw_project.settings import BASE_DIR

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.ini")

config = configparser.ConfigParser()
config.read(config_path)


def get_mongodb():
    mongo_user = config.get("DB", "user")
    mongodb_pass = config.get("DB", "pass")
    db_name = config.get("DB", "db_name")
    domain = config.get("DB", "domain")
    uri = f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"""

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi("1"))

    db = client[db_name]
    return db


def get_local_mongodb():
    client = MongoClient("mongodb://localhost")
    db = client.hw_10
    return db


def get_local_sqlite():
    relative_path = "db.sqlite3"
    sqlite_path = os.path.join(BASE_DIR, relative_path)
    conn = sqlite3.connect(sqlite_path)
    return conn


def print_msg():
    print("HELLO!")
