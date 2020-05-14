from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired, EqualTo, Email 
import email_validator

class SignUp(FlaskForm):
  username = StringField('Username:', validators=[InputRequired()])
  email = StringField('Email:', validators=[Email(), InputRequired()])
  password = PasswordField('New Password:',validators = [InputRequired()])
  confirm = PasswordField('Repeat Password:')
  submit = SubmitField('Sign Up', render_kw={'class': 'btn red waves-effect waves-orange white-text'})


class LogIn(FlaskForm):
  username = StringField('Username', validators=[InputRequired()])
  password = PasswordField('New Password', validators=[InputRequired()])
  submit = SubmitField('Login', render_kw={'class': 'btn red waves-effect waves-orange white-text'})



class AddIngredient(FlaskForm):
  name = StringField('Name:', validatiors=[InputRequired()])
  amount = language = SelectField('Amount', choices=[('1', '1'), ('2', '2'), ('3', '3')])
  checked = BooleanField(default="checked")
  add = SubmitField('Add', render_kw={'class': 'btn red waves-effect waves-orange white-text'})
