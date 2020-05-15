import json
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
import email_validator
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 
from flask_jwt import JWT, jwt_required, current_identity


from models import db, User, Ingredient, Recipe
from forms import SignUp, LogIn, AddIngredient

''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

''' End Flask Login Functions '''

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SECRET_KEY'] = "MYSECRET"
  login_manager.init_app(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
db.create_all(app=app)
''' End Boilerplate Code '''

def authenticate(uname, password):
  user = User.query.filter_by(username=uname).first()
  if user and user.check_password(password):
    return user

def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)

@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LogIn()
  if form.validate_on_submit(): # respond to form submission
    data = request.form
    user = User.query.filter_by(username = data['username']).first()
    if user and user.check_password(data['password']): # check credentials
      flash('Logged in successfully.') # send message to next page
      login_user(user) # login the user
      return redirect(url_for('myList')) # redirect to main page if login successful
    else:
      flash('Invalid username or password') # send message to next page
      return redirect(url_for('login')) # redirect to login page if login unsuccessful
  return render_template('login.html', form=form)


@app.route('/database', methods=['GET', 'POST'])
def database():
  users = User.query.all()
  users = [user.toDict() for user in users]
  return json.dumps(users)


@app.route('/identify')
@jwt_required()
def protected():
    return json.dumps(current_identity.username)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignUp()
  if form.validate_on_submit():
    data = request.form # get data from form submission
    # added and indented
    try:
      newuser = User(username=data['username'], email=data['email']) # create user object
      newuser.set_password(data['password']) # set password
      db.session.add(newuser) # save new user
      db.session.commit()
      flash('Account Created!')# send message
      return redirect(url_for('login'))# redirect to login page
    # added
    except:
      flash('Account Exists')# send message
      db.session.rollback()
    
  return render_template('signup.html', form=form)


@app.route('/ingredients', methods=['GET', 'POST'])
@login_required
def myList():
  ingredientsList = Ingredient.query.filter_by(user_id=current_user.id).all()

  if ingredientsList is None:
      ingredientsList = []

  form = AddIngredient()

  if form.validate_on_submit():
    data = request.form
    newIngredient = Ingredient(name=data['name'], amount=data['amount'], checked=False, user_id=current_user.id)
    db.session.add(newIngredient)
    db.session.commit()
    flash('Ingredient Added!')
    return redirect(url_for('myList'))

  return render_template('ingredients.html', form=form, ingredients=ingredientsList)

@app.route('/ingredient/<id>', methods=['POST'])
@login_required
def delete_ingredient(id):
  remove = Ingredient.query.filter_by(user_id=current_user.id, id=id).first() # retrieve ingredient to remove
  if remove == None:
    return 'Invalid id or unauthorized'
  db.session.delete(remove) # delete the ingredient
  db.session.commit()
  flash('Ingredient Deleted!')
  return redirect(url_for('myList'))

@app.route('/editIngredient/<id>', methods=['GET','POST'])
@login_required
def edit_ingredient(id):
  data = request.form
  if data:
    ingredient = Ingredient.query.filter_by(user_id=current_user.id, id=id).first()
    ingredient.name = data['name']
    ingredient.amount = data['amount']
    db.session.add(ingredient)
    db.session.commit()
    flash('Ingredient Updated!')
    return redirect(url_for('myList'))
  return render_template('edit.html', id=id)


@app.route('/recipes', methods=['GET', 'POST'])
@login_required
def myRecipes():
  
  return render_template('recipes.html')

'''
@app.route('/recipes/addIngredients', methods=['GET', 'POST'])
@login_required
def myRecipes():
  return render_template('recipes.html')

@app.route('/recipes/<id>', methods=['GET', 'POST'])
@login_required
def myRecipes():
  return render_template('recipes.html')

@app.route('/recipes', methods=['GET', 'POST'])
@login_required
def myRecipes():
  return render_template('recipes.html')


@app.route('/recipes', methods=['GET', 'POST'])
@login_required
def myRecipes():
  return render_template('recipes.html')

'''

app.run(host='0.0.0.0', port=8080, debug=True)