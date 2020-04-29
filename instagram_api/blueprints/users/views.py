from flask import Blueprint, Flask, jsonify, render_template, request, make_response
from models.user import User
from app import csrf
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from werkzeug.security import generate_password_hash, check_password_hash
from instagram_api.blueprints.users.mail import send_after_signup_success
import json
from models.item import Item

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


@users_api_blueprint.route('/all', methods=['GET'])
def get_all_users():
    users = User.select()
    result = []
    for user in users:
        result.append({"name": user.username})
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])


@users_api_blueprint.route('/delete', methods=['POST'])
@csrf.exempt
def delete():
    user_id = request.get_json()
    user = User.get_or_none(User.id == user_id['id'])
    user.delete_instance()
    return jsonify({"username": user.username, "message": ["username is deleted"]})


@users_api_blueprint.route('/signup', methods=['POST'])
@csrf.exempt
def sign_up():
    data = request.get_json()
    print(data)
    # json_parse = json.loads(data)
    # print(json_parse)

    username_input = data['username']
    email_input = data['email']
    password_input = data['password']
    user = User(username=username_input,
                password=password_input, email=email_input)

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
        send_after_signup_success(email_input)
        return jsonify({"auth_token": access_token, "message": "Successfully created a user and signed in.", "status": "Success", "user": {"id": registered_user.id, "username": registered_user.username, "Admin_status": registered_user.isAdmin, "email": registered_user.email}}), 200

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400
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
            return jsonify({"auth_token": access_token, "message": "Login Success", "status": "Success", "user": {"id": user.id, "username": user.username, "email": user.email, "Admin_status": user.isAdmin}}), 200
    return jsonify({"message": "Some error occur", "status": "failed"})


@users_api_blueprint.route("/add_item", methods=["POST"])
@csrf.exempt
@jwt_required
def add_item():
    data = request.get_json()
    print(data)
    item_name_input = data['name']
    product_type_input = data['product_type']
    size_input = data['size']
    price_input = data['price']
    image_input = data['image']
    stock_input = data['stock']
    # remember to make function for stock decrease on buy confirm

    item = Item(name=item_name_input, product_type=product_type_input,
                size=size_input, price=price_input, image=image_input, stock=stock_input)

    if item_name_input == "" or product_type_input == "" or size_input == "" or price_input == "" or image_input == "" or stock_input == "":
        return jsonify({'message': 'All fields required', 'status': 'failed'}), 400

    elif item.save():

        return jsonify({"message": "Successfully added item.", "status": "Success"}), 200

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400
