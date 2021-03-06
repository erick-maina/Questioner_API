"""
This contains the endpoints for users
"""
# third party imports
from flask import Flask, jsonify, request, Response, json, abort, make_response, current_app
from marshmallow import ValidationError
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)

# standard imports
from werkzeug.security import check_password_hash

# local imports
from ..models.user_models import UserModel
from ..schemas.user_schema import UserSchema
from ...v2 import v2


@v2.route('/auth/signup', methods=['POST'])
def create_user():
    """ Endpoint to create a new user"""
    json_data = request.get_json()

    """Checks if there's data and if it's in json format"""
    if not json_data:
        abort(make_response(
            jsonify({'status': 400, 'message': 'Sorry but the data provided should be in json'}), 400))

    """Checks if all the required fields have been filled"""
    data, errors = UserSchema().load(json_data)
    if errors:
        abort(make_response(jsonify(
            {'status': 400, 'message': 'Empty field. Please fill all required fields', 'errors': errors}), 400))

        """Checks if a similar username exists"""
    elif UserModel().check_exist('username', json_data['username']):
        abort(make_response(
            jsonify({'status': 400, 'message': 'Username has Already taken'}), 400))

        """Checks if a similar email exists"""
    elif UserModel().check_exist('email', json_data['email']):
        abort(make_response(
            jsonify({'status': 400, 'message': 'Email Already exists'}), 400))

    """Registers the new user and automatically logs them in"""
    result = UserModel().create_user(json_data)
    access_token = create_access_token(identity=result['user_id'])
    return jsonify({'status': 201, 'data': [{'token': access_token, 'user': result}]}), 201


@v2.route('/auth/login', methods=['POST'])
def login():
    """ Endpoint to login a user"""
    json_data = request.get_json()

    """Checks if there's data and if it's in json format"""
    if not json_data:
        abort(make_response(
            jsonify({'status': 400, 'message': 'Sorry but the data provided should be in json'}), 400))

    """Checks if the user exists"""
    if not UserModel().check_exist("username", json_data['username']):
        abort(make_response(
            jsonify({'status': 404, 'message': 'No such user has been registered'}), 404))

    """Checks if the password is correct"""
    response = UserModel().find(json_data['username'])
    if not check_password_hash(response['password'], json_data['password']):
        abort(make_response(
            jsonify({'status': 400, 'message': 'Incorrect password'}), 400))

        """Logs in the user"""
    else:
        access_token = create_access_token(identity=response['user_id'])

        return jsonify({'status': 200, 'data': [{'token': access_token, 'user': response}]}), 200
