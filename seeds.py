import json
from datetime import datetime

import connect
from models import Author, Quote


def seeds_authors():
    with open("authors.json") as json_file:
        authors = json.load(json_file)

    for author in authors:
        Author(
            fullname=author["fullname"],
            born_date=datetime.strptime(author["born_date"], "%B %d, %Y"),
            born_location=author["born_location"],
            description=author["description"],
        ).save()


def seeds_quotes():
    with open("quotes.json") as json_file:
        quotes = json.load(json_file)

    for quote in quotes:
        author_name = quote["author"]
        author = Author.objects(fullname=author_name).first()

        Quote(content=quote["quote"], author=author, tags=quote["tags"]).save()


if __name__ == "__main__":
    seeds_authors()
    seeds_quotes()
