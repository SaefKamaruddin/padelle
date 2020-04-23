from flask import Blueprint, Flask, jsonify, render_template, request, make_response, redirect
from models.item import Item
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from instagram_api.helpers import upload_file_to_aws
from app import csrf


items_api_blueprint = Blueprint('items_api',
                                __name__,
                                template_folder='templates')


@items_api_blueprint.route("/", methods=["POST"])
@csrf.exempt
def upload():
    file = request.files.get("img")
    result = upload_file_to_aws(file)
    return result
