import redis
from mongoengine import connect
from models import Authors, Quotes
import random
import connect

# з'єднання з Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0)


def search_author(name):
    """Пошук автора та цитати в MongoDB"""
    author = Authors.objects(fullname=name).first()
    if author is not None:
        quotes = Quotes.objects(author=author)
        result = "\n".join([quote.quote for quote in quotes])
        redis_client.hset("search_results", name, result)
        return result
    else:
        return f"No author found with name {name}"


def search_tag(tag):
    """Пошук цитат з тегом: MongoDB"""
    quotes = Quotes.objects(tags=tag)
    if quotes:
        result = "\n".join([quote.quote for quote in quotes])
        redis_client.hset("search_results", tag, result)
        return result
    else:
        return f"No quotes found with tag {tag}"


def search_by_tags(tags):
    """Пошук цитат за випадковим тегом зі списку тегів"""
    tag_name = random.choice(tags)
    result = redis_client.hget("search_results", tag_name)
    if result is not None:
        return result.decode("utf-8")
    else:
        return search_tag(tag_name)


def process_input(input_str):
    """Обробка вводу користувача"""
    command = input_str.split(":")
    if command[0] == "name":
        author_name = command[1].strip()
        result = redis_client.hget("search_results", author_name)
        if result is not None:
            return result.decode("utf-8")
        else:
            return search_author(author_name)
    elif command[0] == "tag":
        tag_name = command[1].strip()
        result = redis_client.hget("search_results", tag_name)
        if result is not None:
            return result.decode("utf-8")
        else:
            return search_tag(tag_name)
    elif command[0] == "tags":
        searching_tags = command[1].strip().split(",")
        return search_by_tags(searching_tags)
    elif command[0] == "exit":
        return "Bye!"
    else:
        return "Invalid command"


if __name__ == "__main__":
    while True:
        input_str = input("Input command:")
        result = process_input(input_str)
        print(result)
        if result.lower() == "exit!":
            break
