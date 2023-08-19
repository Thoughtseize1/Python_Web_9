from bson import ObjectId
from django import template

from useful_quotes.utils import get_local_mongodb, print_msg

register = template.Library()


def get_author(id_):
    db = get_local_mongodb()
    author = db.authors.find_one({"_id": ObjectId(id_)})
    return author["fullname"]


""" .для работы с SQL LITE """
# def get_author(id_):
#     try:
#         author = Author.objects.get(id=id_)
#         return author.fullname
#     except Author.DoesNotExist:
#         return None

register.filter("author", get_author)