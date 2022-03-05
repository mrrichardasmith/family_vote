from datetime import datetime
from enum import unique
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin

# Models are classes that create objects which are used to move data to and from the database
# the Model class includes the query property
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(65), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=False)
    password_hash = db.Column(db.String(120))
    posts = db.relationship('Post', backref='user.id', lazy='dynamic')
    Thinking = db.relationship('Thinking', backref='', lazy='dynamic')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 
  
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studying = db.Column(db.String(140))
    country = db.Column(db.String(140))
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.description)

class Thinking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thinking_about = db.Column(db.String(140))
    country = db.Column(db.String(20))
    thoughts = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    username = db.Column(db.String, db.ForeignKey('user.username'))
    

    def __repr__(self):
        return '<Thinking {}>'.format(self.username)

class Day_school(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    yourday = db.Column(db.String(10))
    why = db.Column(db.String(20))
    username = db.Column(db.String, db.ForeignKey('user.username'))

    def __repr__(self):
        return '<Day_school {}>'.format(self.why)
    

@login.user_loader 
def load_user(id): 
  return User.query.get(int(id))