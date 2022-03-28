import email
from flask import Flask, make_response, request, session
import json
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from sklearn.datasets import make_regression
from schema import Athlete, Emails
from athlete_login import athlete_login
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key='SECRET_KEY' #TODO: change it!
app.config['MONGODB_SETTINGS'] =  {
    'db': 'test_db',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
app.session_interface = MongoEngineSessionInterface(db)
db.init_app(app)


def verify_session(func):
    def wrapper(*args, **kwargs):
        if not session.get('email'):
            return json.dumps({'Error': 'UnAuthorized'}), 401, {'ContentType': 'application/json'}
        return func(*args, **kwargs)
    return wrapper
    
@app.route('/logout', methods=['GET', 'POST'])
def athlete_logout():
    session.pop('email')
    resp = make_response(json.dumps({'Success': True}), 200, {'ContentType': 'application/json'})
    return resp

@app.route('/testupdate', methods=["POST"])
def test_update():
    athlete_email = session['email']
    try:
        Athlete.objects(email=athlete_email).update(__raw__=[
            {"$set": {"availability."+"20220329" : "Dublin"}},
            {"$set": {"availability."+"20220330" : "Dublin"}}
        ],)
    except:
        return json.dumps({'Error': 'Update error'}), 500, {'ContentType': 'application/json'}
    resp = make_response(json.dumps({'Success': True}), 200, {'ContentType': 'application/json'})
    return resp


@app.route('/login', methods=['POST'])
def athlete_login():
    athlete_email = request.form['email']
    athlete_password = request.form['password']
    #check if already present in session
    if session.get('email') == athlete_email:
        return make_response(json.dumps({'Success': True, 'status': 'logged in already'}), 200, {'ContentType': 'application/json'})
    athlete = Athlete.objects(email= athlete_email)[0]
    if check_password_hash(athlete.password, athlete_password):
        session['email'] =  athlete_email
        # session['name'] = "name"
        # print(session_id)
        resp = make_response(json.dumps({'Success': True}), 200, {'ContentType': 'application/json'})
        return resp
    else:
        return json.dumps({'Error': 'Incorrect username or password'}), 400, {'ContentType': 'application/json'}



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
    password_hash = generate_password_hash(password)

    try:
        try:
            Emails(
                email= athlete_email
            ).save()
        except:
            return json.dumps({'Error': 'user with email id already exists'}), 500, {'ContentType': 'application/json'}    
        # if len(Athlete.objects(email=athlete_email)) > 0:
        #     return json.dumps({'Error': 'user with email id already exists'}), 500, {'ContentType': 'application/json'}    
        Athlete(name=athlete_name,
                email=athlete_email,
                password=password_hash,
                nationality=nationality,
                location=location).save()
    # except NotUniqueError:
    #     return json.dumps({'Error': 'ahtlete already exists with same email'}), 400, {'ContentType': 'application/json'}
    except Exception as e:
        print(e)
        # print(e.__name__)
        print(e.__class__.__name__)
        print(e.__class__.__qualname__)

        return json.dumps({'Error': 'internal server error'}), 500, {'ContentType': 'application/json'}
    
    return json.dumps({'Success': True}), 200, {'ContentType': 'application/json'}
    #save


if __name__ == "__main__":
    app.run(debug=True)