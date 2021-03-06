from flask import Blueprint, Flask, jsonify, render_template, request, make_response, redirect
from models.item import Item
from models.cart import Cart
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from instagram_api.utils.helpers import upload_file_to_aws
from app import csrf
import datetime
import re


items_api_blueprint = Blueprint('items_api',
                                __name__,
                                template_folder='templates')


@items_api_blueprint.route('/<id>', methods=['GET'])
def get_one_Item(id):
    item = Item.get_or_none(id=id)
    return jsonify({"id": item.id, "name": item.name, "type": item.product_type,
                    "size": item.size, "color": item.color, "price": item.price, "image": item.image, "stock": item.stock, "image_url": item.image_url})


@items_api_blueprint.route('/same/<name>', methods=['GET'])
def get_all_same_name(name):
    print("name")
    items = Item.select().where(Item.name == name)

    return jsonify([{"id": item.id, "name": item.name, "type": item.product_type,
                     "size": item.size, "color": item.color, "price": item.price, "image": item.image, "stock": item.stock, "image_url": item.image_url} for item in items])


@items_api_blueprint.route('/unique', methods=['GET'])
def get_distinct():
    items = Item.select().distinct(Item.name, Item.product_type)

    return jsonify([{"id": item.id, "name": item.name, "type": item.product_type,
                     "size": item.size, "color": item.color, "price": item.price, "image": item.image, "stock": item.stock, "image_url": item.image_url} for item in items])


@items_api_blueprint.route('/items', methods=['GET'])
def get_all_item():
    items = Item.select()

    return jsonify([{"id": item.id, "name": item.name, "type": item.product_type,
                     "size": item.size, "color": item.color, "price": item.price, "image": item.image, "stock": item.stock, "image_url": item.image_url} for item in items])


@items_api_blueprint.route('/delete/name', methods=['POST'])
@csrf.exempt
def delete_by_name():
    data = request.get_json()
    item_name = data['name']
    name = Item.select().where(Item.name == item_name)
    cart_unpaid = Cart.delete().where((Cart.item.in_(name))
                                      & (Cart.payment_status == False))
    cart_paid = Cart.update(item_id=None).where((Cart.item.in_(name))
                                                & (Cart.payment_status == True))
    cart_paid.execute()
    cart_unpaid.execute()
    item = Item.get_or_none(Item.name == item_name)
    item.delete().where(Item.name == item_name).execute()
    return jsonify({"name": item.name, "message": ["item is deleted"]})


@items_api_blueprint.route('/delete/id', methods=['POST'])
@csrf.exempt
def delete_by_id():
    data = request.get_json()
    item_id = data['id']
    item = Item.get_or_none(Item.id == item_id)
    cart = Cart.delete().where(Cart.item_id == item_id, Cart.payment_status == False)
    cart.execute()
    item.delete_instance()
    return jsonify({"id": item.id, "message": ["item is deleted"]})


@items_api_blueprint.route("/add_item", methods=["POST"])
@csrf.exempt
@jwt_required
def add_item():
    data = request.get_json()
    print(data)
    item_name_input = data['name']
    product_type_input = data['product_type']
    size_input = data['size']
    color_input = data['color']
    price_input = data['price']
    image_input = data['image']
    stock_input = data['stock']
    # remember to make function for stock decrease on buy confirm

    item = Item(name=item_name_input, product_type=product_type_input,
                size=size_input, color=color_input, price=price_input, image=image_input, stock=stock_input)

    if item_name_input == "" or product_type_input == "" or size_input == "" or price_input == "" or image_input == "" or stock_input == "":
        return jsonify({'message': 'All fields required', 'status': 'failed'}), 400

    elif item.save():

        return jsonify({"message": "Successfully added item.", "status": "Success"}), 200

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


# need to get image url from aws
@items_api_blueprint.route("/upload_item_image", methods=["POST"])
# to add url to item list
@jwt_required
@csrf.exempt
def upload():
    file = request.files.get("img")
    result = upload_file_to_aws(file)
    item = Item
    item.image = result
    return result


##########################################
###########UPDATE & EDIT INFO#############
##########################################
@items_api_blueprint.route("/name/<id>", methods=["POST"])
@csrf.exempt
def edit_item_name(id):
    data = request.get_json()
    item = Item.get_by_id(id)
    name_input = data['name']

    if name_input == "":
        return jsonify({'message': 'name must not be blank', 'status': 'failed'}), 400

    elif item.update(name=name_input, updated_at=datetime.datetime.now()).where(Item.id == id).execute():
        return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


@items_api_blueprint.route("/product_type/<id>", methods=["POST"])
@csrf.exempt
def edit_item_product_type(id):
    data = request.get_json()
    item = Item.get_by_id(id)
    product_type_input = data['product_type']

    if product_type_input == "":
        return jsonify({'message': 'Field must not be blank', 'status': 'failed'}), 400

    elif item.update(product_type=product_type_input, updated_at=datetime.datetime.now()).where(Item.id == id).execute():
        return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


@items_api_blueprint.route("/size/<id>", methods=["POST"])
@csrf.exempt
def edit_item_size(id):
    data = request.get_json()
    item = Item.get_by_id(id)
    size_input = data['size']

    if size_input == "":
        return jsonify({'message': 'Field must not be blank', 'status': 'failed'}), 400

    elif item.update(size=size_input, updated_at=datetime.datetime.now()).where(Item.id == id).execute():
        return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


@items_api_blueprint.route("/color/<id>", methods=["POST"])
@csrf.exempt
def edit_item_color(id):
    data = request.get_json()
    item = Item.get_by_id(id)
    color_input = data['color']

    if color_input == "":
        return jsonify({'message': 'Field must not be blank', 'status': 'failed'}), 400

    elif item.update(color=color_input, updated_at=datetime.datetime.now()).where(Item.id == id).execute():
        return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


@items_api_blueprint.route("/price/<id>", methods=["POST"])
@csrf.exempt
def edit_item_price(id):
    data = request.get_json()
    item = Item.get_by_id(id)
    price_input = data['price']

    if price_input == "":
        return jsonify({'message': 'Field must not be blank', 'status': 'failed'}), 400

    elif item.update(price=price_input, updated_at=datetime.datetime.now()).where(Item.id == id).execute():
        return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


@items_api_blueprint.route("/image/<id>", methods=["POST"])
@csrf.exempt
def edit_item_image(id):
    data = request.get_json()
    item = Item.get_by_id(id)
    image_input = data['image']

    if image_input == "":
        return jsonify({'message': 'Field must not be blank', 'status': 'failed'}), 400

    elif item.update(image=image_input, updated_at=datetime.datetime.now()).where(Item.id == id).execute():
        return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400


def has_int(word):
    return re.search("[0-9]", word)


def has_alphabet(word):
    return re.search("[\D]", word)


@items_api_blueprint.route("/stock/<id>", methods=["POST"])
@csrf.exempt
def edit_item_stock(id):
    data = request.get_json()
    item = Item.get_by_id(id)
    stock_input = data['stock']

    if stock_input == "":
        return jsonify({'message': 'Field must not be blank', 'status': 'failed'}), 400

    if has_alphabet(stock_input):
        return jsonify({'message': 'Must not contain alphabets', 'status': 'failed'}), 400

    if not has_int(stock_input):
        return jsonify({'message': 'Must contain numbers', 'status': 'failed'}), 400

    elif item.update(stock=stock_input, updated_at=datetime.datetime.now()).where(Item.id == id).execute():
        return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Some error happened", "status": "Failed"}), 400
