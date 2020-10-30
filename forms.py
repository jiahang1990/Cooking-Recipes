from wtforms import StringField, PasswordField, FloatField, IntegerField, SelectField
from wtforms.validators import InputRequired, Optional, Length, Email, NumberRange, DataRequired
#from wtforms_alchemy import ModelForm, Unique
from utils.validators import Unique, Nonexist
from flask_wtf import FlaskForm
from models import User

class UserAddForm(FlaskForm):
    """Form to sign up user"""

    username = StringField('Username', validators=[DataRequired(), Unique(User,User.username, message = 'This username already exsits, please login')])
    email = StringField('E-mail', validators=[DataRequired(), Unique(User, User.email, message = 'This email already exists'), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])


class LoginForm(FlaskForm):
    """Form to sign up user"""
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired(), Unique(User, User.username, message = 'This username already exsits, please use a different name')])
    email = StringField('E-mail', validators=[DataRequired(), Unique(User, User.email, message = 'This email already exists'), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirmpassword = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    image_url = StringField('(Optional) User profile')

    height = FloatField('Height')
    weight = FloatField('Weight')
    gender = SelectField('Gender', choices = [('Male','M'),('Female','M')])
    age = IntegerField('Age', validators = [NumberRange(min=0, max=100, message="Age is not valid")])
