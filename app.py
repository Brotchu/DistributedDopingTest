from flask import Flask
import json
from flask_mongoengine import MongoEngine
from pymysql import Date

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] =  {
    'db': 'test_db',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)


class DateAvailability(db.EmbeddedDocument):
    date = db.DateTimeField(required = True)
    location = db.StringField(required =True)


class Athlete(db.Document):
    name = db.StringField(required = True)
    email = db.StringField(unique = True, required = True)
    password = db.StringField(required = True) #TODO: hash it!!
    nationality = db.StringField(required = True)
    location = db.StringField(required = True)
    # availability = db.ListField(db.EmbeddedDocumentField(DateAvailability))
    availability = db.DictField()
    


@app.route('/')
def hello():
    #TODO: sample user
    Athlete(name="test_athlete1",
            email="test_athlete_email1",
            password="test_password",
            nationality="Ireland",
            location="Dublin").save()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


if __name__ == "__main__":
    app.run(debug=True)