from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re
from playhouse.hybrid import hybrid_property


class Item(BaseModel):
    name = pw.CharField(null=False)
    product_type = pw.CharField(null=False)
    size = pw.CharField(null=False)
    color = pw.CharField(null=False, default=False)
    price = pw.DecimalField(decimal_places=2)
    image = pw.CharField(null=True)
