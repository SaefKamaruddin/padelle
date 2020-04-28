import os
from flask import request
import requests


def send_after_payment(receiver_email):
    return requests.post(
        "https://api.mailgun.net/v3/" +
        os.environ.get("MAILGUN_DOMAIN")+"/messages",
        auth=("api", os.environ.get('MAILGUN_API')),
        data={"from": "Excited User <mailgun@MAILGUN_DOMAIN>",
              "to": ["{receiver_email}"],
              "subject": "Payment",
              "text": "Thank you "})


def send_after_signup_success(receiver_email):
    return requests.post(
        "https://api.mailgun.net/v3/" +
        os.environ.get("MAILGUN_DOMAIN")+"/messages",
        auth=("api", os.environ.get('MAILGUN_API')),
        data={"from": "Excited User <mailgun@" + os.environ.get("MAILGUN_DOMAIN") + ">",
              "to": ["{receiver_email}"],
              "subject": "Sign up",
              "text": "Welcome"
              })
