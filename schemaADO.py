from enum import unique

from mongoengine import (DateTimeField, DictField, Document, EmbeddedDocument,
                         StringField)


class ADO(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)  # TODO: hash it!!

    meta = {'collection': 'ado'}


class Emails(Document):
    email = StringField(required=True, unique=True)
