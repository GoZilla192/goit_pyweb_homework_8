import connect
from models import Author, Quote
from mongoengine.queryset.queryset import QuerySet


def get_quotes_for_tags_startswith(tag: str):
    return Quote.objects(tags__regex=f"^{tag}")


def get_quotes_for_tags(tags: list[str]) -> QuerySet:
    quotes = Quote.objects(tags__in=tags)
    if not quotes:
        return get_quotes_for_tags_startswith(tags[0])

    return quotes


def get_author_for_names_startswith(name: str):
    return Author.objects(fullname__regex=f"^{name}")


def get_quotes_for_names(names: list[str]) -> list[Quote]:
    authors = Author.objects(fullname__in=names)
    if not authors:
        authors = get_author_for_names_startswith(names[0])

    quotes_to_return = []
    for author in authors:
        quotes = Quote.objects(author=author)
        for quote in quotes:
            quotes_to_return.append(quote)

    return quotes_to_return


def display_quotes(quotes: QuerySet | list[Quote]) -> None:
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
        "tag": get_quotes_for_tags,
        "tags": get_quotes_for_tags,
        "name": get_quotes_for_names,
        "names": get_quotes_for_names,
    }

    main()
