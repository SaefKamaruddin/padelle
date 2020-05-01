from flask import Blueprint, Flask, jsonify, render_template, request, make_response
from models.user import User
from app import csrf
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from werkzeug.security import generate_password_hash, check_password_hash
import braintree
import os


payment_api_blueprint = Blueprint('payment_api',
                                  __name__,
                                  template_folder='templates')


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get('BT_MERCHANT_ID'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY ')
    )
)


@payment_api_blueprint.route('/new_payment', methods=['POST'])
def new_payment():
    client_token = gateway.client_token.generate()
    return render_template("payment.html", client_token=client_token)


@payment_api_blueprint.route('/checkout', methods=['POST'])
@csrf.exempt
@jwt_required
def checkout():
    # get current user.id, payment_status = False> true
    print(request.form.get('paymentMethodNonce'))
    result = gateway.transaction.sale({
        # variable for total amount of cost of products in cart
        "amount": request.form["amount"],
        "payment_method_nonce": request.form.get('paymentMethodNonce'),
        "options": {
            "submit_for_settlement": True
        }
    })

    print(result)

    return "Paid"
