from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

# use a form to create new user
@users_blueprint.route('/', methods=['POST'])
def create():
    user = User.create(username=request.form["username"],
                       email=request.form["email"], password=request.form["password"])

    # if login fail
    if len(user.errors) > 0:
        return render_template('users/new.html', errors=user.errors)
    else:
        return redirect(url_for("homepage"))

    # if login succeeds, to be changed


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
