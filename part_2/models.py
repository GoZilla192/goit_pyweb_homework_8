from mongoengine import Document
from mongoengine.fields import StringField, EmailField, EnumField, BooleanField

from custom_enums import PreferredNotify
import connect_to_mongodb

class Contact(Document):
    fullname = StringField()
    email = EmailField()
    phone = StringField(max_length=(15))
    preferred_notify = EnumField(PreferredNotify, default=PreferredNotify.EMAIL)
    message_is_send = BooleanField(default=False)
