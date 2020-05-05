import os
from flask import request
import requests


def send_after_payment(receiver_email):
    return requests.post(
        "https://api.mailgun.net/v3/" +
        os.environ.get("MAILGUN_DOMAIN")+"/messages",
        auth=("api", os.environ.get('MAILGUN_API')),
        data={"from": "Padelle <mailgun@MAILGUN_DOMAIN>",
              "to": receiver_email,
              "subject": "Payment",
              "text": "Thank you "})
# remember to attch to payment


def send_after_signup_success(receiver_email):

    return requests.post(
        "https://api.mailgun.net/v3/" +
        os.environ.get("MAILGUN_DOMAIN")+"/messages",
        auth=("api", os.environ.get('MAILGUN_API')),
        data={"from": "Padelle <mailgun@" + os.environ.get("MAILGUN_DOMAIN") + ">",
              "to": receiver_email,
              "subject": "Sign up",
              "text": "Welcome"
              })