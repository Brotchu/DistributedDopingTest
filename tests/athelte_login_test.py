# from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from schema import Athlete, Emails
from app import app, db
import json


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
    athl1 = {
        'name' : 'athlete1',
        'password': 'Password1',
        'confirm_password' : 'Password1',
        'email' : 'testuser006@gmail.com',
        'nationality' : 'IRL',
        'location' : 'Dublin'
    }

    athl2 = {
        'name' : 'athlete1',
        'password': 'Password1',
        'confirm_password' : 'Password1',
        'email' : 'testuser0061@gmail.com',
        'nationality' : 'IRL',
        'location' : 'Dublin'
    }
    log_in_user_not_found = {
        'password' : 'Password1',
        'email' : 'ssharma1@gmail.com'
    }

    log_in = {
        'password' : 'Password1',
        'email' : 'testuser005@gmail.com'
    }

    log_in_password_missing = {
        'password' : '',
        'email' : 'testuser005@gmail.com'
    }

    log_in_email_missing = {
        'password' : 'Password1',
        'email' : ''
    }

    def test_user_unsuccessful_login(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='application/json',data=json.dumps(self.athl))
        # Check for correct validation error
        res_code = response.status_code
        
        if res_code == 200:
            response = tester.post('/login', content_type='application/json',data=json.dumps(self.log_in))
    
            res_code = response.status_code
            assert res_code == 200
        else:
            assert res_code == 200
        print(response)

    # def test_user_unsuccessful_notFound(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/register', content_type='multipart/form-data',data=self.athl2)
    #     # Check for correct validation error
    #     res_code = response.status_code
        
    #     if res_code == 200:
    #         response = tester.post('/login', content_type='multipart/form-data',data=self.log_in_user_not_found)
    
    #         res_code = response.status_code
    #         assert res_code == 200
    #     else:
    #         assert res_code == 200
    #     print(response)
    
