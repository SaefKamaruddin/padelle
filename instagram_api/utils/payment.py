from flask import Blueprint, Flask, jsonify, render_template, request, make_response
from models.user import User
from models.payment import Payment
from models.cart import Cart
from models.item import Item
from app import csrf
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from werkzeug.security import generate_password_hash, check_password_hash
import braintree
import os
from instagram_api.utils.mail import send_after_payment
import operator


payment_api_blueprint = Blueprint('payment_api',
                                  __name__,
                                  template_folder='templates')


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get('BT_MERCHANT_ID'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY')
    )
)


@payment_api_blueprint.route('/new_payment', methods=['GET'])
@csrf.exempt
def new_payment():
    client_token = gateway.client_token.generate()
    return render_template("payment2.html", token=client_token)
    # return jsonify({"client token": client_token})


@payment_api_blueprint.route('/checkout', methods=['POST'])
@csrf.exempt
@jwt_required
def checkout():
    current_id = User.get_by_id(get_jwt_identity())
    not_enough_items = Cart.select().join(Item).where(Cart.user == current_id,
                                                      Cart.payment_status == False, Cart.amount > Item.stock)

    if len(not_enough_items) > 0:
        return jsonify("Message: There are not enough of these items in stock",
                       [{"item":
                         {"id": item.item.id,
                          "stock": item.item.stock,
                          "color": item.item.color,
                          "name": item.item.name,
                          "product_type": item.item.product_type,
                          "image": item.item.image_url,
                          "price": item.item.price,
                          "size": item.item.size}}
                           for item in not_enough_items], "Please reduce amount", {"Status": "Failed"}), 400

    else:
        print(request.form.get('paymentMethodNonce'))
        data = request.get_json()
        amount_input = data['amount']
        pmNonce_input = data['paymentMethod']

        result = gateway.transaction.sale({
            "amount": amount_input,
            "payment_method_nonce": pmNonce_input,
            "options": {
                "submit_for_settlement": True
            }
        })

        Payment(user=current_id, Braintree_Transaction_id=result.transaction.id,
                Total_amount=result.transaction.amount).save()

        Cart.update(payment_status=True).where(
            Cart.user == current_id, Cart.payment_status == False).execute()

    print(result.transaction)
    print(result.transaction.id)
    print(result.transaction.amount)
    send_after_payment(current_id.email)

    return jsonify({'message': 'Success', 'status': 'success'}), 200


# @payment_api_blueprint.route('/checkout', methods=['POST'])
# @csrf.exempt
# def checkout():

#     print(request.form.get('paymentMethodNonce'))
#     nonce = request.form.get("bt-nonce")

#     result = gateway.transaction.sale({
#         "amount": "10.00",
#         "payment_method_nonce": nonce,
#         "options": {
#             "submit_for_settlement": True
#         }
#     })
#     print(result.transaction)
#     print(result.transaction.id)
#     print(result.transaction.amount)

#     return jsonify({'message': 'Success', 'status': 'success'}), 200


@payment_api_blueprint.route('/test', methods=['POST'])
@csrf.exempt
@jwt_required
def match():
    current_id = User.get_by_id(get_jwt_identity())
    carts = Cart.select().where(
        Cart.user == current_id, Cart.payment_status == False)
    # not_enough_items = Cart.select().join(Item).where(Cart.user == current_id,
    #                                                   Cart.payment_status == False, Cart.amount > Item.stock)

    # print(len(not_enough_items))

    Cart.update({Cart.item.stock: (Cart.item.stock-Cart.amount)}).where(Cart.user == current_id,
                                                                        Cart.payment_status == False).execute()  # Execute the query, returning number of rows updated.

    # print(([{
    #     "id": cart.user.id,
    #     "amount": cart.amount,
    #     "item id": cart.item.id,
    #     "stock": cart.item.stock}
    #     for cart in carts]))
    # print([cart.amount for cart in carts])
    # print([cart.item.stock for cart in carts])

    # amount_bought = [cart.amount for cart in carts]
    # stock_remainder = [cart.item.stock for cart in carts]
    # remainder = list(map(operator.sub, stock_remainder, amount_bought))

    # cart_afterpay.update(Cart.item.stock == (Cart.item.stock - Cart.amount)
    #                      ).where(Cart.user == cart_afterpay, Cart.payment_status == False).execute()

    return jsonify([{"id": cart.user.id,
                     "amount": cart.amount,
                     "item id": cart.item.id,
                     "stock": cart.item.stock}for cart in carts])

    # return jsonify([{"user": {
    #                 "id": item.user.id,
    #                 "username": item.user.username},
    #     "cart": {"id": item.id,
    #              "amount": item.amount},
    #     "item":
    #     {"id": item.item.id,
    #      "stock": item.item.stock,
    #      "color": item.item.color,
    #      "name": item.item.name,
    #      "product_type": item.item.product_type,
    #      "image": item.item.image_url,
    #      "price": item.item.price,
    #      "size": item.item.size}}
    #     for item in not_enough_items])

    # return jsonify("Message: There are not enough of these items in stock",
    #                [{"item":
    #                  {"id": item.item.id,
    #                   "stock": item.item.stock,
    #                   "color": item.item.color,
    #                   "name": item.item.name,
    #                   "product_type": item.item.product_type,
    #                   "image": item.item.image_url,
    #                   "price": item.item.price,
    #                   "size": item.item.size}}
    #                    for item in not_enough_items], "Please reduce amount", {"Status": "Failed"}), 400

    # remainder = list(map(operator.sub, stock, amount))
    # return jsonify(print(remainder))
    # if [{cart.amount}for cart in carts] > [{cart.item.stock}for cart in carts]:

    #     print("out of stock")
    #     return jsonify([{cart.amount, cart.item.stock}
    #                     for cart in carts])

    # else:
    #     return jsonify([{"user": {
    #         "id": cart.user.id,
    #         "username": cart.user.username},
    #         "cart": {"id": cart.id,
    #                  "amount": cart.amount},
    #         "item":
    #         {"id": cart.item.id,
    #          "color": cart.item.color,
    #          "name": cart.item.name,
    #          "product_type": cart.item.product_type,
    #          "image": cart.item.image_url,
    #          "price": cart.item.price,
    #          "size": cart.item.size}}
    #         for cart in carts])
