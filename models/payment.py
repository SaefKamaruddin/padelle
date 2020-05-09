import peewee as pw
from models.user import User
from models.base_model import BaseModel


class Payment(BaseModel):
    user = pw.ForeignKeyField(User, backref="user")
    Braintree_Transaction_id = pw.CharField(null=True)
    Total_amount = pw.DecimalField(null=True)
    # Fx to add and remove item from cart
    # SUM of all unpaid into a cart
    # IF paid make payment status=true AND give receipt number
