from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    recipes = db.relationship('Recipe', backref='user', lazy=True)
    ingredients = db.relationship('Ingredient', backref='user', lazy=True)

    def toDict(self):
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password":self.password
      }
    
    #hashes the password parameter and stores it in the object
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    #Returns true if the parameter is equal to the object's password property
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    #To String method
    def __repr__(self):
        return '<User {}>'.format(self.username)  

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    readyInMins = db.Column(db.Integer, nullable=False)
    imageURL = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def toDict(self):
        return{
            "id": self.id,
            "title": self.title,
            "mins": self.readyInMins,
            "image": self.imageURL
        }


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    checked = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def toDict(self):
      return{
        "id": self.id,
        "name": self.name,
        "amount": self.amount,
        "checked": self.checked,
        "user_id": self.user_id
      }
