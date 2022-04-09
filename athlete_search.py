from flask import Blueprint, request, jsonify
import json
from schema import Athlete

app_search_blueprint = Blueprint('app', __name__)


#TODO: verify admin wrapper
@app_search_blueprint.route('/getAthleteLocationForDate', methods=['POST'])
def get_athlete_for_date():
    athlete_email = request.form['email']
    search_date = request.form['date']

    # result = Athlete.objects(email=athlete_email).scalar("name", "availability."+search_date)
    try:
        result = Athlete.objects(email=athlete_email).scalar("availability")
    except Exception as e:
        return json.dumps({'Error': 'data read issue'}), 400, {'ContentType': 'application/json'}
    if len(result) == 0 :
        return json.dumps({'Error': 'No athlete with given email id found'}), 400, {'ContentType': 'application/json'}
    return json.dumps(result[0][search_date])


@app_search_blueprint.route('/getAthletesInLocation', methods=['POST'])
def get_athletes_for_location():
    location = request.form['location']
    search_date = request.form['date']

    try:
        result = Athlete.objects(__raw__= {'availability.'+search_date+'.location': location})
    except:
        return json.dumps({'Error': 'not sure'}), 400, {'ContentType': 'application/json'}
    if len(result) == 0:
        return json.dumps({'Error': 'No athletes found for given date and location'}), 400, {'ContentType': 'application/json'}
    
    return jsonify(result)