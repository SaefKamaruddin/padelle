import peewee as pw
from models.item import Item
from models.user import User
from models.base_model import BaseModel


class Cart(BaseModel):
    user_id = pw.ForeignKeyField(User)
    item_id = pw.ForeignKeyField(Item)
    payment_status = pw.BooleanField(null=False, default=False)
    receipt_number = pw.IntegerField(null=True)
    amount = pw.IntegerField(null=True)
    # Fx to add and remove item from cart
    # SUM of all unpaid into a cart
    # IF paid make payment status=true AND give receipt number
