from schema import Athlete
from flask import request, Blueprint
import json
from werkzeug.security import check_password_hash
athlete_login_blueprint = Blueprint('app', __name__)

@athlete_login_blueprint.route('/login', methods=['POST'])
def athlete_login():
    athlete_email = request.form['email']
    athlete_password = request.form['password']
    # athlete = Athlete.query.filter_by(email = athlete_email).first()
    athlete = Athlete.objects(email= athlete_email)[0]
    if check_password_hash(athlete.password, athlete_password):
        # session[athlete_email]
        return json.dumps({'Success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'Error': 'Incorrect username or password'}), 400, {'ContentType': 'application/json'}

# {
#     '20220324' : 'Dublin'
# }