# from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from schema import Athlete, Emails
from app import app, db

app.config['MONGODB_SETTINGS'] =  {
    'db': 'TestCasesDB',
    'host': '127.0.0.1',
    'port': 27017
}

db.init_app(app)

with app.app_context():
    Athlete().drop_collection()
    Emails().drop_collection()

class TestAthleteRegistration:

    athlete = {
        'name' : 'athlete1',
        'password': 'Password1',
        'confirm_password' : 'Password1',
        'email' : 'testuser1@gmail.com',
        'nationality' : 'IRL',
        'location' : 'Dublin'
    }

    def test_athlete_registration(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data', data=self.athlete)

        print(response)
        
        res_code = response.status_code
        assert res_code == 200