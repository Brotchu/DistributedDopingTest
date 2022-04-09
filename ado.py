from flask import Blueprint

app_test_blueprint = Blueprint('app', __name__)

@app_test_blueprint.route('/ping')
def ping():
    return "pong"


# Athlete:
'''
register
login
add availability // add time of day
update availibility
'''

# ADO:
'''
admin login
search athletes avaiable location for a date 
search athletes within a location for a date
'''