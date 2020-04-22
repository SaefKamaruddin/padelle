from flask import Blueprint, Flask, jsonify, render_template, request, make_response
from models.user import User
from app import csrf
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from werkzeug.security import generate_password_hash, check_password_hash


users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"


@users_api_blueprint.route('/<id>', methods=['GET'])
def get_one_User(id):
    user = User.get_or_none(id=id)
    return jsonify({"username": user.username}, {"email": user.email})


@users_api_blueprint.route('/signup', methods=['POST'])
@csrf.exempt
def sign_up():
    data = request.get_json()
    print(data)
    hashed_password = generate_password_hash(data['password'])
    username_input = data['username']
    email_input = data['email']
    password_input = data['password']
    user = User(username=username_input,
                password=password_input, email=email_input)

    username_check = User.get_or_none(User.username == username_input)
    email_check = User.get_or_none(User.email == email_input)

    if username_input == "" or password_input == "" or email_input == "":
        return jsonify({'message': 'All fields required', 'status': 'failed'})

    elif username_check:
        return jsonify({"message": ["username is already in use"], "status": "failed"})

    elif email_check:
        return jsonify({"message": ["Email is already in use"], "status": "failed"})

    elif user.save():
        access_token = create_access_token(identity=username_input)

        registered_user = User.get(User.username == username_input)
        print(registered_user)
        return jsonify({"auth_token": access_token, "message": "Successfully created a user and signed in.", "status": "Success", "user": {"id": registered_user.id, "username": registered_user.username}})

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"})
####################

# api for user log in
@users_api_blueprint.route('/login', methods=['POST'])
@csrf.exempt
def login():
    user_login = request.get_json()
    print(user_login)
    user = User.get_or_none(User.username == user_login['username'])

    if user:
        check_password = user_login['password']
        hashed_password = user.password
        result = check_password_hash(hashed_password, check_password)

        if result:
            access_token = create_access_token(identity=user.id)
            return jsonify({"auth_token": access_token, "message": "Login Success", "status": "Success", "user": {"id": user.id, "username": user.username, "email": user.email}})
    return jsonify({"message": "Some error occur", "status": "failed"})
