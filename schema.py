from enum import unique
from mongoengine import Document, EmbeddedDocument, StringField, DictField, DateTimeField


class DateAvailability(EmbeddedDocument):
    date = DateTimeField(required = True)
    location = StringField(required =True)


class Athlete(Document):
    name = StringField(required = True)
    email = StringField(required = True)
    password = StringField(required = True) #TODO: hash it!!
    nationality = StringField(required = True)
    location = StringField(required = True)
    # availability = db.ListField(db.EmbeddedDocumentField(DateAvailability))
    availability = DictField()

    meta = {'collection' : 'athlete'}

class Emails(Document):
    email = StringField(required=True, unique = True)