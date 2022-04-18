from flask import Flask, request, jsonify, Blueprint, session
import json
from flask_mongoengine import MongoEngine
from pymysql import Date
from os import environ
from schemaADO import ADO
app_loginADO = Blueprint('app_loginADO',__name__)
from werkzeug.security import check_password_hash


@app_loginADO.route('/login_ado', methods=['GET', 'POST'])
def ado_login():
    ado_email = request.form['email']
    ado_password = request.form['password']
    #check if already present in session
    if session.get('email') == ado_email:
        return make_response(json.dumps({'Success': True, 'status': 'logged in already'}), 200, {'ContentType': 'application/json'})
    ado = ADO.objects(email= ado_email)[0]
    if check_password_hash(ado.password, ado_password):
        session['email'] =  ado_email
        # session['name'] = "name"
        # print(session_id)
        return json.dumps({'Success': True}), 200, {'ContentType': 'application/json'}

        return resp
    else:
        return json.dumps({'Error': 'Incorrect username or password'}), 400, {'ContentType': 'application/json'}

app_logoutADO = Blueprint('app_logoutADO',__name__)

@app_logoutADO.route('/logout_ado', methods=['GET', 'POST'])
def ado_logout():
    session.pop('email')
    return json.dumps({'Success': True}), 200, {'ContentType': 'application/json'}
    return resp