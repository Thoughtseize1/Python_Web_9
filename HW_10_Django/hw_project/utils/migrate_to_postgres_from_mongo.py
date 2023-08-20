import os
import django
from pymongo import MongoClient

from useful_quotes.utils import get_local_mongodb

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hw_project.settings')
django.setup()

from useful_quotes.models import Quote, Tag, Author

mongo_database = get_local_mongodb()
authors = mongo_database.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author["fullname"],
        born_date=author["born_date"],
        born_location=author["born_location"],
        description=author["description"]
    )

quotes = mongo_database.quotes.find()

for mongo_quote in quotes:
    tags = []
    for tag in mongo_quote["tags"]:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)
    exist_quote = bool(len((Quote.objects.filter(quote=mongo_quote['quote']))))
    if not exist_quote:
        mongo_author = mongo_database.authors.find_one({'_id': mongo_quote['author']})
        a = Author.objects.get(fullname=mongo_author["fullname"])
        q = Quote.objects.create(
            quote=mongo_quote['quote'],
            author=a
        )
        for tag in tags:
            q.tags.add(tag)
