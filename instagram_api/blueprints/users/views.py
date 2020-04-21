from flask import Blueprint, Flask, jsonify, render_template, request
from models.user import User

users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"


@users_api_blueprint.route('/<id>', methods=['GET'])
def getUser(id):
    user = User.get_or_none(id=id)
    return jsonify({"username": user.username}, {"email": user.email})


@users_api_blueprint.route('/signup', methods=['POST'])
def signup():
