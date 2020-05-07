from flask import Blueprint, Flask, jsonify, render_template, request, make_response
from models.user import User
from models.payment import Payment
from models.cart import Cart
from app import csrf
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from werkzeug.security import generate_password_hash, check_password_hash
import braintree
import os
from instagram_api.utils.mail import send_after_payment


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
@jwt_required
def new_payment():
    client_token = gateway.client_token.generate()
    return jsonify({"client token": client_token})


@payment_api_blueprint.route('/checkout', methods=['POST'])
@csrf.exempt
@jwt_required
def checkout():
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

    current_id = User.get_by_id(get_jwt_identity())
    Payment(user=current_id, Braintree_Transaction_id=result.transaction.id,
            Total_amount=result.transaction.amount).save()

    Cart.update(payment_status=True).where(
        Cart.user == current_id, Cart.payment_status == False).execute()

    print(result.transaction)
    print(result.transaction.id)
    print(result.transaction.amount)
    send_after_payment(current_id.email)

    return jsonify({'message': 'Success', 'Amount Paid': (result.transaction.amount), 'status': 'success'}), 200

