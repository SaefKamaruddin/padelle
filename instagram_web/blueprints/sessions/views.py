from flask import Blueprint, render_template, session, flash, request, url_for, redirect
# from helpers.render import render
from werkzeug.security import check_password_hash
# from flask_login import login_user, logout_user, login_required
from models.user import User

sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")


@sessions_blueprint.route("/")
def new():
    return render_template("sessions/new.html")


# @sessions_blueprint.route("/", method=["POST"])
# def create():
#     username = request.form.get("username")
#     user = User.get_or_none(User.username == username)

    # if user and check_password_hash(user.password, password):
    #     flash("Welcome!", "success")
    #     login_user(user)
    #     session["user_id"] = user.id
    #     return redirect(url_for("homepage"))

    # else:
    #     flash("Bad login")
    #     return render("sessions/new.html" ,username=username)


# @sessions_blueprint.route("/logout", methods=["POST"])
# @login_required
# def destroy():
#     flash("logged out")
#     logout_user()
#     return redirect(url_for("homepage"))
