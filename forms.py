from flask_wtf import Form
from wtforms_sqlalchemy.orm import model_form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, Length, EqualTo,
                                ValidationError, Email)

from old_models import *


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('A User with that username already exists.')

def email_exists(form, field):
    if User.select().where(User.email ==field.data).exists():
        raise ValidationError('User with that email exists already.')

class RegistrationForm(Form):
    first_name = StringField(
        'First Name',
        validators = [DataRequired(), Length(max=50),]
    )
    last_name = StringField(
        'Last Name',
        validators = [DataRequired(), Length(max=100),]
    )
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, numbers, and"
                         " underscores only.")
            ),
            name_exists,
        ])
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
            Length(max=255),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators = [DataRequired()]
    )

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])

class ProjectForm(Form):
    title = StringField(
        'Title',
        validators = [
            DataRequired(),
            Length(min=20)
        ])
    description = TextAreaField(
        'Give more details on the project',
        validators = [DataRequired()])
