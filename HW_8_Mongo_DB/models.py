from mongoengine import *
from connect import connect


class Authors(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField(max_length=100))
    quote = StringField(required=True)
    author = ReferenceField(Authors, required=True, reverse_delete_rule=CASCADE)
