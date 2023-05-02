import json
from bson import ObjectId
from mongoengine import *
from models import Authors, Quotes


with open("auhtors.json", encoding="utf-8") as f:
    authors_data = json.load(f)

with open("quotes.json", encoding="utf-8") as f:
    quotes_data = json.load(f)


for author_data in authors_data:
    author = Authors(
        fullname=author_data["fullname"],
        born_date=author_data.get("birthday"),
        born_location=author_data.get("born_location"),
        description=author_data.get("description"),
    )
    author.save()

for quote_data in quotes_data:
    author = Authors.objects.get(fullname=quote_data["author"])
    new_quote = Quotes(
        tags=quote_data["tags"], quote=quote_data["quote"], author=author
    )
    new_quote.save()
