from schemaADO import ADO
from flask import request
import json
from werkzeug.security import check_password_hash


def ado_login():
    ado_email = request.form['email']
    ado_password = request.form['password']
   
    ado = ADO.objects(email= ado_email)[0]
    if check_password_hash(ado.password, ado_password):
        return json.dumps({'Success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'Error': 'Incorrect username or password'}), 400, {'ContentType': 'application/json'}

