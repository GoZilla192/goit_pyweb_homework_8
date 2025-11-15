from configparser import ConfigParser
from pathlib import Path
import pika


config = ConfigParser()
config.read(Path(__file__).parent / "config.ini")

user = config["RABITMQ"].get("user")
password = config["RABITMQ"].get("password")
port = config["RABITMQ"].get("port")
vhost = config["RABITMQ"].get("vhost")


def get_connection():
    credentials = pika.PlainCredentials("snbbrqvq", "kecW1OwVTG0asM5icZLJmyFwbAUirrww")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="kebnekaise.lmq.cloudamqp.com",
            port=5672,
            credentials=credentials,
            virtual_host="snbbrqvq",
        )
    )

    return connection
