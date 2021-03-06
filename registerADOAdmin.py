import json
from os import environ

from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, Flask, jsonify, request, session
from flask_mongoengine import MongoEngine
from werkzeug.security import check_password_hash, generate_password_hash

# from app import db
from schemaADO import ADO, Emails

# from ado_login import ado_login

app_registerADO = Blueprint('app', __name__)


@app_registerADO.route("/register_ado", methods=['POST'])
def register_ados():
    if request.method != 'POST':
        return json.dumps({'Error': 'method not allowed'}), 405, {'ContentType': 'application/json'}

    # get info from form
    reqBody = request.get_json()

    ado_name = reqBody['name']
    ado_email = reqBody['email']
    ado_password = reqBody['password']
    ado_confirm_password = reqBody['confirm_password']
    if not ado_name:
        return json.dumps({'Error': 'required  Name'}), 400, {'ContentType': 'application/json'}
    elif not ado_email:
        return json.dumps({'Error': 'required  Email'}), 400, {'ContentType': 'application/json'}

    if ado_password != ado_confirm_password:
        return json.dumps({'Error': 'password and confirm password does not match'}), 400, {'ContentType': 'application/json'}
    # TODO: hash password
    ado_password_hash = generate_password_hash(ado_password)

    # create ado object

    try:
        try:
            Emails(
                email=ado_email
            ).save()
        except:
            return json.dumps({'Error': 'ado with email id already exists'}), 500, {'ContentType': 'application/json'}

        ADO(name=ado_name,
            email=ado_email,
            password=ado_password_hash).save()
    except NotUniqueError:
        return json.dumps({'Error': 'ADO already exists with same email'}), 400, {'ContentType': 'application/json'}
    except Exception as e:
        print(e)
        # print(e.__name__)
        print(e.__class__.__name__)
        print(e.__class__.__qualname__)

        return json.dumps({'Error': 'internal server error'}), 500, {'ContentType': 'application/json'}

    return json.dumps({'Success': True}), 200, {'ContentType': 'application/json'}
    # save
