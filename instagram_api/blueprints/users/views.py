from flask import Blueprint, Flask, jsonify, render_template, request, make_response
from models.user import User
from app import csrf
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from werkzeug.security import generate_password_hash, check_password_hash
from instagram_api.utils.mail import send_after_signup_success, add_list_member
import os
import datetime
from models.base_model import BaseModel
import re

#####Password validation######


def has_lower(word):
    return re.search("[a-z]", word)


def has_upper(word):
    return re.search("[A-Z]", word)


def has_special(word):
    return re.search("[\W]", word)


####routing####
users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')

###Retrieving USER information##
@users_api_blueprint.route('/', methods=['GET'])
def index():

    return "USERS API"


@users_api_blueprint.route('/user', methods=['GET'])
@jwt_required
def get_one_User():
    user = User.get_by_id(get_jwt_identity())
    return jsonify({"username": user.username, "email": user.email, "address": user.address, "zipcode": user.zipcode, "country": user.country, "mail_list": user.mailing_list})


@users_api_blueprint.route('/all', methods=['GET'])
def get_all_users():
    users = User.select()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email, "address": user.address, "zipcode": user.zipcode, "country": user.country, "mail": user.mailing_list} for user in users])


@users_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def my_info():
    user = User.get_by_id(get_jwt_identity())
    print(get_jwt_identity())
    print(user.id)
    print(user.email)
    return jsonify({"id": user.id, "email": user.email, "username": user.username})


@users_api_blueprint.route('/check_name/<name>', methods=['GET'])
@csrf.exempt
def check_name(name):
    if User.select().where(User.username == name):
        return jsonify({"username": name, "message": "This username exists"})

    else:
        return jsonify({"message": "username is available"})

        ###################################################
        ###################################################
        ###################################################
        ###################################################
        # SIGNUP/Login Function


@users_api_blueprint.route('/signup', methods=['POST'])
@csrf.exempt
def sign_up():
    data = request.get_json()
    print(data)
    username_input = data['username']
    email_input = data['email']
    password_input = data['password']
    mail_input = data['mailing_list']
    user = User(username=username_input,
                password=password_input, email=email_input, mailing_list=mail_input)

    username_check = User.get_or_none(User.username == username_input)
    email_check = User.get_or_none(User.email == email_input)

    if username_input == "" or password_input == "" or email_input == "":
        return jsonify({'message': 'All fields required', 'status': 'failed'}), 400

    elif username_check:
        return jsonify({"message": ["username is already in use"], "status": "failed"}), 400

    elif email_check:
        return jsonify({"message": ["Email is already in use"], "status": "failed"}), 400

    elif user.save():
        access_token = create_access_token(identity=username_input)

        registered_user = User.get(User.username == username_input)
        print(registered_user)
        print(email_input)
        print(registered_user.mailing_list)
        send_after_signup_success(email_input)

        if registered_user.mailing_list == True:
            print("hello")
            add_list_member(receiver_email=email_input,
                            username=username_input)

        return jsonify({"auth_token": access_token, "message": "Successfully created a user and signed in.", "status": "Success", "user": {"id": registered_user.id, "username": registered_user.username, "Admin_status": registered_user.isAdmin, "email": registered_user.email, "mailing_list": registered_user.mailing_list}}), 200

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


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
            return jsonify({"auth_token": access_token, "message": "Login Success", "status": "Success", "user": {"id": user.id, "username": user.username, "email": user.email, "Admin_status": user.isAdmin}}), 200
    return jsonify({"message": "Some error occur", "status": "failed"}), 400


###################################################
###########EDITING USER INFORMATION################
###################################################

@users_api_blueprint.route('/delete', methods=['POST'])
@csrf.exempt
def delete():
    user_id = request.get_json()
    user = User.get_or_none(User.id == user_id['id'])
    user.delete_instance()
    return jsonify({"username": user.username, "message": ["username is deleted"]})


@users_api_blueprint.route('/address', methods=['POST'])
@jwt_required
@csrf.exempt
def add_address():
    user_id = User.get_by_id(get_jwt_identity())
    data = request.get_json()
    address_input = data['address']
    country_input = data['country']
    zipcode_input = data['zipcode']
    user = User(address=address_input,
                country=country_input, zipcode=zipcode_input)

    if address_input == "" or country_input == "" or zipcode_input == "":
        return jsonify({'message': 'All fields required', 'status': 'failed'}), 400

    elif user.update(address=address_input,
                     country=country_input, zipcode=zipcode_input, updated_at=datetime.datetime.now()).where(User.id == user_id).execute():
        return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


@users_api_blueprint.route('/username', methods=['POST'])
@jwt_required
@csrf.exempt
def edit_username():
    user_id = User.get_by_id(get_jwt_identity())
    user = User.get_or_none(User.id == user_id)
    data = request.get_json()
    username_input = data['username']

    username_check = User.get_or_none(User.username == username_input)

    if username_input == "":
        return jsonify({'message': 'Username must not be blank', 'status': 'failed'}), 400

    elif username_check:
        return jsonify({"message": ["username is already in use"], "status": "failed"}), 400

    elif user.update(username=username_input, updated_at=datetime.datetime.now()).where(User.id == user_id).execute():
        return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


@users_api_blueprint.route('/password', methods=['POST'])
@jwt_required
@csrf.exempt
def edit_password():
    data = request.get_json()
    user_id = User.get_by_id(get_jwt_identity())
    user = User.get_or_none(User.id == user_id)
    print(user)
    password_input = data['password']

    if password_input == "":
        return jsonify({'message': 'password must not be blank', 'status': 'failed'}), 400

    elif len(password_input) < 6:
        return jsonify({'message': 'password must be at least 6 characters', 'status': 'failed'}), 400

    elif not has_lower(password_input):
        return jsonify({'message': ' Passwords needs at least one lowercase character', 'status': 'failed'}), 400

    elif not has_upper(password_input):
        return jsonify({'message': ' Passwords needs at least one uppercase character', 'status': 'failed'}), 400

    elif not has_special(password_input):
        return jsonify({'message': ' Passwords needs at least one special character', 'status': 'failed'}), 400

    elif user.update(password=generate_password_hash(password_input), updated_at=datetime.datetime.now()).where(User.id == user_id).execute():

        return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


@users_api_blueprint.route('/email_list', methods=['POST'])
@csrf.exempt
@jwt_required
def edit_mailing_list():
    current_id = User.get_by_id(get_jwt_identity())
    if current_id.mailing_list == True:
        print(current_id.mailing_list)
        current_id.update(mailing_list=False).execute()
        return jsonify({"message": "You have been removed from the mailing list", "status": "success"}), 200

    elif current_id.mailing_list == False:
        current_id.update(mailing_list=True).execute()
        return jsonify({"message": "You have been added to the mailing list", "status": "success"}), 200
