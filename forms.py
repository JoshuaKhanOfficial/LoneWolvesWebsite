from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import InputRequired, EqualTo, Email 
import email_validator

class SignUp(FlaskForm):
  username = StringField('Username', validators=[InputRequired()])
  email = StringField('Email', validators=[Email(), InputRequired()])
  password = PasswordField('New Password',validators = [InputRequired()])
  confirm = PasswordField('Repeat Password')
  submit = SubmitField('Sign Up', render_kw={'class': 'btn red waves-effect waves-orange white-text'})


class LogIn(FlaskForm):
  username = StringField('Username', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired()])
  submit = SubmitField('Login', render_kw={'class': 'btn red waves-effect waves-orange white-text'})


class AddIngredient(FlaskForm):
  name = StringField('Name:', validators=[InputRequired()])
  amount = IntegerField('Amount', validators=None)
  submit = SubmitField('Add', render_kw={'class': 'btn waves-effect waves-light white-text'})


  
  