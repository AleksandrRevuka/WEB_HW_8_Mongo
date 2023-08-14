import sys
import redis
from redis_lru import RedisLRU

import connect
from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def get_quotes_by_author(author_name):
    author = Author.objects(fullname__istartswith=author_name).first()

    if author:
        quotes = Quote.objects(author=author)
        return quotes
    else:
        return []


@cache
def get_quotes_by_tag(tag):
    quotes = Quote.objects(tags__istartswith=tag)
    return quotes


@cache
def get_quotes_by_tags(tags):
    tags_list = tags.split(",")
    quotes = Quote.objects(tags__in=tags_list)
    return quotes


def main():
    while True:
        input_data = input(">>> ").strip()
        pars_input_data = [data.strip() for data in input_data.split(":")]
        command = pars_input_data[0]
        argument = pars_input_data[1] if len(pars_input_data) > 1 else ""

        if command == "name":
            quotes = get_quotes_by_author(argument)
            for quote in quotes:
                print(quote.content)

        elif command == "tag":
            quotes = get_quotes_by_tag(argument)
            for quote in quotes:
                print(quote.content)

        elif command == "tags":
            quotes = get_quotes_by_tags(argument)
            for quote in quotes:
                print(quote.content)

        elif command == "exit":
            sys.exit()
        else:
            print("Invalid command. Please enter name, tag, tags or exit.")


if __name__ == "__main__":
    main()
