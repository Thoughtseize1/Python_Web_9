from mongoengine import *
from connect import connect


class Authors(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=50)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField(max_length=30))
    quote = StringField(max_length=500, required=True)
    author = ReferenceField(Authors, required=True, reverse_delete_rule=CASCADE)
