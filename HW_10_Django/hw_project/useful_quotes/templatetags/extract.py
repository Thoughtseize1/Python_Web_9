from bson import ObjectId
from django import template

from useful_quotes.utils import get_local_mongodb, print_msg

register = template.Library()


@register.filter
def get_author(author):
    return author.fullname


@register.filter
def extract_tags(quote):
    return quote.tags.all()
