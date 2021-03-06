import peewee as pw
from models.item import Item
from models.user import User
from models.payment import Payment
from models.base_model import BaseModel


class Cart(BaseModel):
    user = pw.ForeignKeyField(User, backref="cart_user", null=True)
    item = pw.ForeignKeyField(
        Item, backref="cart_item", null=True, on_delete='SET NULL')
    payment_status = pw.BooleanField(null=False, default=False)
    payment = pw.ForeignKeyField(Payment, backref="payment", null=True)
    amount = pw.IntegerField(null=False, default=1)
    # Fx to add and remove item from cart
    # SUM of all unpaid into a cart
    # IF paid make payment status=true AND give receipt number
