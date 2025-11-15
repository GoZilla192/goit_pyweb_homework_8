import connect
from models import Author, Quote
from mongoengine.queryset.queryset import QuerySet

from caching_redis import (
    set_quotes_by_author_names_cache,
    set_quotes_by_tag_cache,
    get_quotes_by_author_names_cache,
    get_quotes_by_tags_cache,
)


def get_quotes_by_tag(tag: str):
    return Quote.objects(tags__regex=f"^{tag}")


def get_author_by_name(name: str):
    return Author.objects(fullname__regex=f"^{name}")


def get_quotes_by_tags(tags: list[str]) -> QuerySet:
    if quotes := get_quotes_by_tags_cache(tags):
        return [quotes]

    quotes = Quote.objects(tags__in=tags)
    if not quotes:
        return get_quotes_by_tag(tags[0])

    quotes_string = ""
    for quote in quotes:
        quotes_string += "\n" + quote["quote"] if quotes_string else quote["quote"]

    set_quotes_by_tag_cache(tags, {"quote": quotes_string})

    return quotes


def get_quotes_by_author_name(names: list[str]) -> list[Quote]:
    if quotes := get_quotes_by_author_names_cache(names):
        return quotes

    authors = Author.objects(fullname__in=names)
    if not authors:
        authors = get_author_by_name(names[0])

    quotes_to_return = []
    for author in authors:
        quotes = Quote.objects(author=author).exclude("id", "author")
        for quote in quotes:
            quotes_to_return.append(quote.to_mongo().to_dict())

    set_quotes_by_author_names_cache(names, quotes_to_return)
    return quotes_to_return


def display_quotes(quotes: QuerySet | list[Quote] | list[dict]) -> None:
    for quote in quotes:
        print(quote["quote"])


def main():
    while True:
        input_string = input("Enter command: ").strip()
        try:
            command, value = [el.strip() for el in input_string.split(":")]
        except ValueError:
            if input_string == "exit":
                print("Goodbye!")
                break

            print(f'Ivalid command: "{input_string}"')
            continue

        if command not in COMMANDS:
            print(f'Unknown command: "{command}"')
            continue

        args = [el.strip() for el in value.split(",")]
        display_quotes(COMMANDS[command.strip()](args))


if __name__ == "__main__":
    COMMANDS = {
        "tag": get_quotes_by_tags,
        "tags": get_quotes_by_tags,
        "name": get_quotes_by_author_name,
        "names": get_quotes_by_author_name,
    }

    main()
