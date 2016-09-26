import datetime
import bcrypt

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from sqlalchemy import Column, Integer, Text, TypeDecorator
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import validates

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's Requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported at the moment."""
        return False



