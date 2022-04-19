from enum import unique
from mongoengine import Document, EmbeddedDocument, StringField, DictField, DateTimeField
class ADO(Document):
    name = StringField(required = True)
    email = StringField(required = True)
    password = StringField(required = True) #TODO: hash it!!

    meta = {'collection': 'ado'}

class Emails(Document):
    email = StringField(required=True, unique = True)