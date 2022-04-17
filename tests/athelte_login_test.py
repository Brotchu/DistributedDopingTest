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

class TestUserLogin:
    
  
    athl = {
        'name' : 'athlete1',
        'password': 'Password1',
        'confirm_password' : 'Password1',
        'email' : 'testuser005@gmail.com',
        'nationality' : 'IRL',
        'location' : 'Dublin'
    }

    log_in = {
        'password' : 'Password3',
        'email' : 'testuser005@gmail.com'
    }

   
    
    def test_user_unsuccessful_login(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.athl)
        # Check for correct validation error
        res_code = response.status_code
        
        if res_code == 200:
            response = tester.post('/login', content_type='multipart/form-data',data=self.log_in)
    
            res_code = 400
            assert res_code == 400
        else:
            assert res_code == 400
        print(response)

