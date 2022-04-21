# from flask import Flask
import json

from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from schema import Athlete, Emails
from app import app, db
from flask import Flask, jsonify, make_response, request, session, Blueprint


app.config['MONGODB_SETTINGS'] =  {
    'db': 'TestCasesDB',
    'host': '127.0.0.1',
    'port': 27017
}

#db.init_app(app)

with app.app_context():
    Athlete().drop_collection()
    Emails().drop_collection()
#.........................................................................................................#  
def verify_session(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("email"):
            print("in decorator")
            print(session.get("email"))
            return f(*args, **kwargs)
        else:
            return json.dumps({'Error': 'UnAuthorized'}), 401, {'ContentType': 'application/json'}
    return decorated_func
#.........................................................................................................#  

class TestAvailability1:
    #email_ = session.get('email')

    athl = {
        'name' : 'athlete1',
        'password': 'Password1',
        'confirm_password' : 'Password1',
        'email' : 'testuser0052@gmail.com',
        'nationality' : 'IRL',
        'location' : 'Dublin'
    }

    login = {
        
        'password': 'Password1',
       
        'email' : 'testuser0052@gmail.com'
    }
    TestAvailability = {
        
        'email' : 'testuser0052@gmail.com' ,
        'availability':{
            '2021-01-01':'Dublin',
            '2021-01-02':'Cork'
        
        }
    }

   
    def availability_test(self):
        tester = app.test_client(self)
        
        response = tester.post('/register', content_type='application/json',data=json.dumps(self.athl))
        # Check for correct validation error
        res_code = response.status_code
        
        if res_code == 200:
            response = tester.post('/login', content_type='application/json',data=json.dumps(self.login))
    
            res_code = response.status_code
            assert res_code == 200
        else:
            assert res_code == 200

        if res_code == 200:
            response = tester.post('/availability', content_type='application/json',data=json.dumps(self.TestAvailability))
    
            res_code = response.status_code
            assert res_code == 200
        else:
            assert res_code == 200

        print(response)
