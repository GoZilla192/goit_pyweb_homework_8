from configparser import ConfigParser
from faker import Faker
from pathlib import Path
import pika
import random
import pickle

from connect_to_rabitmq import get_connection
from custom_enums import PreferredNotify
from models import Contact


config = ConfigParser()
config.read(Path(__file__).parent / "config.ini")
exchange_for_notifications = config["RABITMQ"].get("EXCHANGE_FOR_NOTIFICATIONS")
queue_for_notify_by_email = config["RABITMQ"].get("QUEUE_FOR_NOTIFY_BY_EMAIL")
queue_for_notify_by_sms = config["RABITMQ"].get("QUEUE_FOR_NOTIFY_BY_SMS")

connection = get_connection()
channel = connection.channel()
channel.exchange_declare(exchange=exchange_for_notifications, exchange_type="direct")
channel.queue_declare(queue=queue_for_notify_by_email, durable=True)
channel.queue_declare(queue=queue_for_notify_by_sms, durable=True)
channel.queue_bind(exchange=exchange_for_notifications, queue=queue_for_notify_by_email)
channel.queue_bind(exchange=exchange_for_notifications, queue=queue_for_notify_by_sms)

faker = Faker("uk-UA")


def generate_data(n):
    for _ in range(n):
        preferred_notify = random.choice([PreferredNotify.EMAIL, PreferredNotify.SMS])
        contact = Contact(
            fullname=faker.full_name(short=False),
            email=faker.email(),
            phone=''.join([str(random.randint(0,9)) for _ in range(10)]),
            preferred_notify=preferred_notify,
        )
        contact.save()
    
        payload = {"document_id": contact.id}

        match preferred_notify:
            case PreferredNotify.EMAIL:
                channel.basic_publish(
                    exchange=exchange_for_notifications,
                    routing_key=queue_for_notify_by_email,
                    body=pickle.dumps(payload),
                )
                
            case PreferredNotify.SMS:
                channel.basic_publish(
                    exchange=exchange_for_notifications,
                    routing_key=queue_for_notify_by_sms,
                    body=pickle.dumps(payload),
                )
                


    connection.close()


generate_data(20)
