import redis
from configparser import ConfigParser
from pathlib import Path
import json

config = ConfigParser()
config.read(Path(__file__).parent / "config.ini")
host = config.get("REDIS", "host")
port = config.get("REDIS", "port")
password = config["REDIS"].get("password")

connect = redis.Redis(host=host, port=port, password=password)


def set_quotes_by_author_names_cache(names: list[str], query_result: list[dict]):
    connect.set("name:" + "".join(names), json.dumps(query_result))


def set_quotes_by_tag_cache(tags: list[str], query_result: dict):
    connect.set("tag:" + "".join(tags), json.dumps(query_result))


def get_quotes_by_author_names_cache(names: list[str]):
    quotes = connect.get("name:" + "".join(names))
    if not quotes:
        return None

    return json.loads(quotes)


def get_quotes_by_tags_cache(tags: list[str]):
    quotes = connect.get("tag:" + "".join(tags))
    if not quotes:
        return None

    return json.loads(quotes)
