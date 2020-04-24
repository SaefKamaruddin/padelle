from flask import Blueprint, Flask, jsonify, render_template, request, make_response, redirect
from models.item import Item
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from instagram_api.helpers import upload_file_to_aws
from app import csrf


items_api_blueprint = Blueprint('items_api',
                                __name__,
                                template_folder='templates')


@items_api_blueprint.route("/add_item", methods=["POST"])
@csrf.exempt
def add_item():
    data = request.get_json()
    print(data)
    item_name_input = data['name']
    product_type_input = data['product_type']
    size_input = data['size']
    price_input = data['price']
    image_input = data['image']
    stock_input = data['stock']

    item = Item(name=item_name_input, product_type=product_type_input,
                size=size_input, price=price_input, image=image_input, stock=stock_input)

    if item_name_input == "" or product_type_input == "" or size_input == "" or price_input == "" or image_input == "" or stock_input == "":
        return jsonify({'message': 'All fields required', 'status': 'failed'}), 400

    elif item.save():

        return jsonify({"message": "Successfully added item.", "status": "Success"}), 200

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


# need to get image url from aws
@items_api_blueprint.route("/", methods=["POST"])
@csrf.exempt
def upload():
    file = request.files.get("img")
    result = upload_file_to_aws(file)
    return result
