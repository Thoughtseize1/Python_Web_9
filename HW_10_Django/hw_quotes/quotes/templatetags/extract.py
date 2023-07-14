from bson.objectid import ObjectId
from django import template

import sys
import os

# Получаем путь к текущему файлу
script_dir = os.path.dirname(os.path.abspath(__file__))

# Получаем путь к папке quotes
quotes_dir = os.path.dirname(script_dir)

# Получаем путь к папке проекта
project_dir = os.path.dirname(quotes_dir)

# Получаем путь к папке с модулем get_db
get_db_dir = os.path.join(project_dir, "quotes")

# Добавляем путь к папке с модулем в переменную PATH
sys.path.append(get_db_dir)

# Теперь вы можете выполнять импорт модуля get_db
from get_db import get_local_mongodb

register = template.Library()


def get_author(id_):
    db = get_local_mongodb()
    author = db.authors.find_one({"_id": ObjectId(id_)})
    return author["fullname"]


register.filter("author", get_author)
