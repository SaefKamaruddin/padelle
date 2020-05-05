from instagram_api.blueprints.users.cart import cart_api_blueprint
from instagram_api.utils.payment import payment_api_blueprint
from instagram_api.blueprints.users.store_item import items_api_blueprint
from instagram_api.blueprints.users.views import users_api_blueprint
from app import app
from flask_cors import CORS
from flask_jwt_extended import (JWTManager)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)
## API Routes ##


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(items_api_blueprint, url_prefix='/api/v1/items')
app.register_blueprint(payment_api_blueprint, url_prefix='/payment')
app.register_blueprint(cart_api_blueprint, url_prefix='/api/v1/cart')
