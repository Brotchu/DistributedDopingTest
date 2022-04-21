# # from flask import Flask

# import json
# from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
# from schema import Athlete, Emails
# from app import app, db

# app.config['MONGODB_SETTINGS'] =  {
#     'db': 'TestCasesDB',
#     'host': '127.0.0.1',
#     'port': 27017
# }
# db.init_app(app)

# with app.app_context():
#     Athlete().drop_collection()
#     Emails().drop_collection()

# class TestADORegistration:

#     ados = {
#         'ado_name' : 'ado1',
#         'ado_password': 'Password1',
#         'ado_confirm_password' : 'Password1',
#         'ado_email' : 'testuser1@gmail.com',
        
#     }

    

#     def test_ado_registration(self):
#         tester = app.test_client(self)
#         data=json.dumps(self.athlete)
#         response = tester.post('/register_ado', content_type='application/json', data=json.dumps(self.ados))

#         print(response)
        
#         res_code = response.status_code
#         assert res_code == 200