from configparser import ConfigParser
from pathlib import Path
import pickle

from connect_to_rabitmq import get_connection
from custom_enums import PreferredNotify
from models import Contact


config = ConfigParser()
config.read(Path(__file__).parent / "config.ini")
queue_for_notify_by_email = config["RABITMQ"].get("QUEUE_FOR_NOTIFY_BY_EMAIL")

connection = get_connection()
channel = connection.channel()
channel.queue_declare(queue=queue_for_notify_by_email, durable=True)


def send_email(email):
    return True


def callback(ch, method, properties, body):
    contact_id = pickle.loads(body)["document_id"]
    contact = Contact.objects(id=contact_id).first()
    contact.update(message_is_send=True)
    send_email(contact.email)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_for_notify_by_email, on_message_callback=callback)
channel.start_consuming()
