from datetime import datetime
from email.policy import default
from enum import unique
from operator import index
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
    Likesdislikes = db.relationship('Likesdislikes', backref='user.id', lazy='dynamic')
    thinking = db.relationship('Thinking', backref='', lazy='dynamic')
    admin = db.Column(db.String(5))
    housekeeping = db.Column(db.String(5))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 
  
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Likesdislikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes_dislikes = db.Column(db.String(7))
    country = db.Column(db.String(140))
    reason = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    username = db.Column(db.Integer, db.ForeignKey('user.username'))

    def __repr__(self):
        return '<Likesdislikes {}>'.format(self.reason)

class Thinking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thinking_about = db.Column(db.String(140))
    thoughts = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    username = db.Column(db.String, db.ForeignKey('user.username'))
    

    def __repr__(self):
        return '<Thinking {}>'.format(self.username)

class Life_hacks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    hacktitle = db.Column(db.String(120))
    hackdescription = db.Column(db.String(500))
    username = db.Column(db.String, db.ForeignKey('user.username'))

class Day_school(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    yourday = db.Column(db.String(10))
    why = db.Column(db.String(20))
    username = db.Column(db.String, db.ForeignKey('user.username'))

    def __repr__(self):
        return '<Day_school {}>'.format(self.why)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    good = db.Column(db.String(50))
    bad = db.Column(db.String(50))
    ugly = db.Column(db.String(50))
    morewords = db.Column(db.String(120))
    username = db.Column(db.String, db.ForeignKey('user.username'))

    def __repr__(self):
        return '<People {}>'.format(self.morewords)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(db.Boolean)
    

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    rent = db.Column(db.Float)
    housekeeping = db.Column(db.Float)
    water = db.Column(db.Float)
    electric = db.Column(db.Float)
    counciltax = db.Column(db.Float)
    internet = db.Column(db.Float)
    fitness = db.Column(db.Float)
    bakery = db.Column(db.Float)
    shopping = db.Column(db.Float)
    username = db.Column(db.String, db.ForeignKey('user.username'))

class Credits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    salary_deposit = db.Column(db.Float)
    windfall = db.Column(db.Float)


class Workfood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    work_breakfast = db.Column(db.Float)
    work_lunch = db.Column(db.Float)
    after_work_social = db.Column(db.Float)
    work_snacks_me = db.Column(db.Float)
    work_snacks_share = db.Column(db.Float)
    username = db.Column(db.String, db.ForeignKey('user.username'))
    cost = db.Column(db.Float)
  
class Extragroceries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    grocerydescription = db.Column(db.String(500))
    username = db.Column(db.String, db.ForeignKey('user.username'))
    cost = db.Column(db.Float)

class Subscriptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    subscription_name = db.Column(db.String(120))
    subscription_term = db.Column(db.String(10))
    subscription_start_date = db.Column(db.DateTime)
    subscription_auto_renewal = db.Column(db.DateTime, index=True)
    cost = db.Column(db.Float)
    username = db.Column(db.String, db.ForeignKey('user.username'))

class Transport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    destination = db.Column(db.String(120))
    method_of_travel = db.Column(db.String(10))
    cost = db.Column(db.Float)
    username = db.Column(db.String, db.ForeignKey('user.username'))

class Familyentertainment(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    entertainment_title = db.Column(db.String(120))
    entertainmnet_description = db.Column(db.String(500))
    cost = db.Column(db.Float)
    username = db.Column(db.String, db.ForeignKey('user.username'))

class Takeaway(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    takeaway_choice = db.Column(db.String(20))
    takeaway_other = db.Column(db.String(20))
    cost = db.Column(db.Float)
    username = db.Column(db.String, db.ForeignKey('user.username'))

class Investments(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    investment_name = db.Column(db.String(20))
    investment_description = db.Column(db.String(20))
    cost = db.Column(db.Float)
    username = db.Column(db.String, db.ForeignKey('user.username'))


class Insurance(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    insurance_name = db.Column(db.String(20))
    insurance_description = db.Column(db.String(20))
    cost = db.Column(db.Float)
    username = db.Column(db.String, db.ForeignKey('user.username'))

class Rollover(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    rent_fixed = db.Column(db.Float)
    rent_lock_previous = db.Column(db.Boolean)
    rent_lock = db.Column(db.Boolean)
    water_fixed = db.Column(db.Float)
    water_lock_previous = db.Column(db.Boolean)
    water_lock = db.Column(db.Boolean)
    electric_fixed = db.Column(db.Float)
    electric_lock_previous = db.Column(db.Boolean)
    electric_lock = db.Column(db.Boolean)
    counciltax_fixed = db.Column(db.Float)
    counciltax_lock_previous = db.Column(db.Boolean)
    counciltax_lock = db.Column(db.Boolean)
    internet_fixed = db.Column(db.Float)
    internet_lock_previous = db.Column(db.Boolean) 
    internet_lock = db.Column(db.Boolean)
    username = db.Column(db.String, db.ForeignKey('user.username'))




@login.user_loader 
def load_user(id): 
  return User.query.get(int(id))


class Testing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thinking_about = db.Column(db.String(140))
    thoughts = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    username = db.Column(db.String, db.ForeignKey('user.username'))
    

    def __repr__(self):
        return '<Testing {}>'.format(self.username)