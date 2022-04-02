from flask import Flask, request, jsonify
import json
from flask_mongoengine import MongoEngine
from pymysql import Date
from os import environ
from bson.json_util import dumps
from bson.objectid import ObjectId

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
    availability = db.DictField(required = False)

    #def __init__(self, name, email, password, nationality, location, availability):
     #   self.name = name
      #  self.email = email
       # self.password = password
        #self.nationality = nationality
        #self.location = location
        #self.availability = availability






@app.route('/register', methods=['POST'])
def register_athlete():
    if request.method  != 'POST':
        return json.dumps({'Error': 'method not allowed'}), 405, {'ContentType': 'application/json'}
    
    #get info from form
    athlete_name = request.form['name']
    athlete_email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    nationality = request.form['nationality']
    location = request.form['location']
    availability = {}


    if not athlete_name:
        return json.dumps({'Error': 'required Athlete Name'}), 400, {'ContentType': 'application/json'}
    elif not athlete_email:
        return json.dumps({'Error': 'required Athlete Email'}), 400, {'ContentType': 'application/json'}
    elif not nationality:
        return json.dumps({'Error': 'required Athlete Nationality'}), 400, {'ContentType': 'application/json'}
    elif not location:
        return json.dumps({'Error': 'required Athlete Locaiton'}), 400, {'ContentType': 'application/json'}
    elif not password or not confirm_password:
        return json.dumps({'Error': 'required Athlete Password'}), 400, {'ContentType': 'application/json'}
    

    if password != confirm_password:
        return json.dumps({'Error': 'password and confirm password does not match'}), 400, {'ContentType': 'application/json'}
    #TODO: hash password
    #create athlete object

    try:
        Athlete(name=athlete_name,
                email=athlete_email,
                password=password,
                nationality=nationality,
                location=location).save()
    except NotUniqueError:
        return json.dumps({'Error': 'ahtlete already exists with same email'}), 400, {'ContentType': 'application/json'}
    except Exception as e:
        print(e)
        # print(e.__name__)
        print(e.__class__.__name__)
        print(e.__class__.__qualname__)

        return json.dumps({'Error': 'internal server error'}), 500, {'ContentType': 'application/json'}
    
    return json.dumps({'Success': True}), 400, {'ContentType': 'application/json'}
    #save

@app.route("/availability", methods=['POST'])
def availability():
    # response = {}
    object_ = request.get_json()
    # object_old = object_[0]
    print(object_['availability'])
   # for avl in object_['availability']:
    #    print(avl['Day'], avl['Month'], avl['Year'])
    #return 'ok'
    # object_new = object_[1]
    #print(object_new)
    # query = SampleTable.replace_one(object_old, object_new, True)
   
    email_ = "sharmasaubhagya1999@gmail.com"
  
    updateList = []
    for avl in object_['availability']:
        updateDict = {}
        updateDict['$set'] = {'availability.'+avl['Date']: avl['Location']}
        updateList.append(updateDict)
    print(updateList)
    
    Athlete.objects(email=email_).update(__raw__= updateList)

    return jsonify({'Availability is updated!'})

if __name__ == "__main__":
    app.run(debug=True)


    
