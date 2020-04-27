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
    price = pw.IntegerField(null=False)
    image = pw.CharField(null=False)
    stock = pw.IntegerField(null=True)

    @hybrid_property
    def image_url(self):
        from app import app
        if self.image == None:
            return "#"
        else:
            return app.config.get('AWS_S3_DOMAIN') + self.image
