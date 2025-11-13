from mongoengine import Document, CASCADE
from mongoengine.fields import StringField, IntField, ReferenceField, ListField


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField("Author", reverse_delete_rule=CASCADE)
    quote = StringField()
