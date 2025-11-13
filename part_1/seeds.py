import connect
from models import Author, Quote
import json
from pathlib import Path


BASE_PATH = Path(__file__).parent

with open(BASE_PATH / "authors.json") as fp:
    authors_json = json.load(fp)

with open(BASE_PATH / "quotes.json") as fp:
    quotes_json = json.load(fp)


def main():
    author_fields = ["fullname", "born_date", "born_location", "description"]

    for author_dict in authors_json:
        author_values = author_dict.values()
        author = Author(**dict(zip(author_fields, author_values))).save()
        for quote_dict in quotes_json:
            if author.fullname == quote_dict["author"]:
                Quote(tags=quote_dict["tags"], author=author, quote=quote_dict["quote"]).save()


if __name__ == "__main__":
    main()