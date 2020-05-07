from flask import Flask, request
import json
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, User, Todo

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = "MYSECRET"
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) 
    db.init_app(app)
    return app

app = create_app()

app.app_context().push()
db.create_all(app=app)

def authenticate(uname, password):
  user = User.query.filter_by(username=uname).first()
  if user and user.check_password(password):
    return user

def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)

@app.route('/')
def index():
  users = User.query.all()
  users = [user.toDict() for user in users]
  return json.dumps(users)

@app.route('/identify')
@jwt_required()
def protected():
    return json.dumps(current_identity.username)

@app.route('/signup', methods=['POST'])
def signup():
  userdata = request.get_json()
  newuser = User(username=userdata['username'], email=userdata['email'])
  newuser.set_password(userdata['password'])
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError:
    db.session.rollback()
    return 'username or email already exists'
  return 'user created', 201
