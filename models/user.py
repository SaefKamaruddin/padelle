from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re
import jwt

# REGEX for password


def has_lower(word):
    return re.search("[a-z]", word)


def has_upper(word):
    return re.search("[A-Z]", word)


def has_special(word):
    return re.search("[\W]", word)


class User(BaseModel):
    username = pw.CharField(unique=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.TextField(null=False)
    isAdmin = pw.BooleanField(null=False, default=False)
    address = pw.TextField(null=True)
    zipcode = pw.CharField(null=True)
    country = pw.CharField(null=True)
    mailing_list = pw.BooleanField(null=False, default=True)

    # hash passwords

    # def save(self, *args, **kwargs):
    #     self.password = generate_password_hash(self.password)
    #     return super(User, self).save(*args, **kwargs)


# create with used email
# create with unique username
# Password with restrictions at least 6 chars with one special char, one upper and one lower


    def validate(self):
        existing_email = User.get_or_none(email=self.email)
        existing_username = User.get_or_none(username=self.username)

        if existing_email != None:
            self.errors.append("User's email already exists")

        if existing_username != None:
            self.errors.append("Username already taken")

        if len(self.password) < 6:
            self.errors.append(
                "Password needs to be a minimum of 6 characters")

        if not has_lower(self.password):
            self.errors.append(
                "Passwords needs at least one lowercase character")

        if not has_upper(self.password):
            self.errors.append(
                "Passwords needs at least one uppercase character")

        if not has_special(self.password):
            self.errors.append(
                "Passwords needs at least one special character")

        if self.password == '#Admin123':
            self.isAdmin = True

        self.password = generate_password_hash(self.password)
