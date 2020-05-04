from flask import Blueprint, Flask, jsonify, render_template, request, make_response, redirect
from models.item import Item
from models.user import User
from models.cart import Cart
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from app import csrf
import datetime
import json

cart_api_blueprint = Blueprint('cart_api',
                               __name__,
                               template_folder='templates')

# functions: add to cart, remove from cart, afterpayment, change payment to status to True, issue receipt after payment
@cart_api_blueprint.route('/<id>', methods=['GET'])
def get_by_id(id):
    cart = Cart.get_or_none(id=id)
    return jsonify({"id": cart.id,
                    "user id": cart.user.id,
                    "item id": cart.item.id,
                    "date_created": cart.created_at,
                    "last_updated": cart.updated_at,
                    "payment_status": cart.payment_status,
                    "receipt_number": cart.receipt_number,
                    "amount": cart.amount})


@cart_api_blueprint.route('/user/<id>', methods=['GET'])
def get_by_user(id):

    items = (User
             .select()
             .join(Cart)
             .join(Item)
             .where(Cart.user.id == id))

    return jsonify([{"id": item.id, "name": item.username}for item in items])


# @cart_api_blueprint.route('/add_new_item', methods=['POST'])
# @csrf.exempt
# def add_to_cart():
#     data = request.get_json()
#     user_input = data['user']
#     item_input = data['item']

#     cart = Cart(user=user_input, item=item_input)
#     cart_check = Cart.get_or_none(Cart.user == user_input,
#                                   Cart.item == item_input, Cart.payment_status == False)

#     if user_input == "" or item_input == "":
#         return jsonify({'message': 'All fields required', 'status': 'failed'}), 400
#     elif cart_check:
#         cart_check.update(
#             amount=Cart.amount+1, updated_at=datetime.datetime.now()).where(Cart.user_id == user_input,
#                                                                             Cart.item_id == item_input, Cart.payment_status == False).execute()
#         return jsonify({'message': 'Item already exists, added to amount', 'status': 'success'}), 200
#     elif cart.save():
#         return jsonify({'message': 'Item added successfully', 'status': 'success'}), 200

#     else:
#         return jsonify({"message": "Uncaught error", "status": "Failed"}), 400


@cart_api_blueprint.route('/add_new_item', methods=['POST'])
@csrf.exempt
@jwt_required
def add_to_cart():
    data = request.get_json()
    item_input = data['item']
    user_id = User.get_by_id(get_jwt_identity())

    cart = Cart(user=user_id, item=item_input)
    cart_check = Cart.get_or_none(Cart.user == user_id,
                                  Cart.item == item_input, Cart.payment_status == False)

    if item_input == "":
        return jsonify({'message': 'All fields required', 'status': 'failed'}), 400
    elif cart_check:
        cart_check.update(
            amount=Cart.amount+1, updated_at=datetime.datetime.now()).where(Cart.user_id == user_id,
                                                                            Cart.item_id == item_input, Cart.payment_status == False).execute()
        return jsonify({'message': 'Item already exists, added to amount', 'status': 'success'}), 200
    elif cart.save():
        return jsonify({'message': 'Item added successfully', 'status': 'success'}), 200

    else:
        return jsonify({"message": "Uncaught error", "status": "Failed"}), 400


@cart_api_blueprint.route('/add/<id>', methods=['POST'])
@csrf.exempt
def add_same_item(id):
    cart = Cart.get_by_id(id)
    if cart.payment_status == True:
        return jsonify({'message': 'This transaction has been completed, create a new cart', 'status': 'failed'}), 400

    elif cart.update(amount=Cart.amount+1, updated_at=datetime.datetime.now()).where(Cart.id == id).execute():
        return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Uncaught error", "status": "Failed"}), 400


@cart_api_blueprint.route('/deduct/<id>', methods=['POST'])
@csrf.exempt
def deduct_same_item(id):
    cart = Cart.get_by_id(id)
    if cart.payment_status == True:
        return jsonify({'message': 'This transaction has been completed, create a new cart', 'status': 'failed'}), 400

    elif cart.update(amount=Cart.amount-1, updated_at=datetime.datetime.now()).where(Cart.id == id).execute():
        if cart.amount < 1:
            cart.delete_instance()
            return jsonify({"Item removed from record": "Update success"})
        else:
            return jsonify({"message": "Update success"})

    else:
        return jsonify({"message": "Uncaught error", "status": "Failed"}), 400


@cart_api_blueprint.route('/delete/id', methods=['POST'])
@csrf.exempt
def delete():
    cart_id = request.get_json()
    cart = Cart.get_or_none(Cart.id == cart_id['id'])
    cart.delete_instance()
    return jsonify({"id": cart.id, "message": ["item is deleted from cart"]})
