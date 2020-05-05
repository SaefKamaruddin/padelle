import peewee as pw
from models.user import User
from models.base_model import BaseModel


class Payment(BaseModel):
    user = pw.ForeignKeyField(User, backref="user")
    payment_status = pw.BooleanField(null=False, default=False)
    Braintree_Transaction_id = pw.CharField(null=False)
    Total_amount = pw.DecimalField(null=False)
    # Fx to add and remove item from cart
    # SUM of all unpaid into a cart
    # IF paid make payment status=true AND give receipt number
