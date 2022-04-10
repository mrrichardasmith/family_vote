from asyncio import transports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateTimeField, RadioField, TextAreaField, DecimalField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class LikesDislikesForm(FlaskForm):
    likes_dislikes = RadioField('Like or Dislike', choices=['Likes', 'Dislikes'], validators=[DataRequired()])
    country = SelectField(u'Country', choices=[('USA', 'United States'), ('UK', 'United Kingdom'), ('EU', 'Europe')])
    reason = StringField('More Words')
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ThinkingForm(FlaskForm):
    thinking_about = StringField('What are you thinking about', validators=[DataRequired()])
    thoughts = StringField('Your thoughts', validators=[DataRequired()])
    submit = SubmitField('Say It')

class LifeHacksForm(FlaskForm):
    hack_title = StringField('Title', validators=[DataRequired()])
    hack_description = TextAreaField('Life Hack Description', validators=[DataRequired()])
    submit = SubmitField('Hack It')

class DaySchoolForm(FlaskForm):
    yourday = RadioField('Your Day Was', choices=['Great', 'OK', 'Blah', 'Ugh!', 'Bad'], validators=[DataRequired()])
    why = StringField('More Words Why', validators=[DataRequired()])
    submit = SubmitField('Day Done')

class GoodBadUglyForm(FlaskForm):
    good = StringField('Was anybody kind or friendly today?')
    bad = StringField('Did anyone make life difficult today?')
    ugly = StringField('Was anybody mean to you today?')
    morewords = TextAreaField('More Words')
    submit = SubmitField('Submit')

class AdminForm(FlaskForm):
    registration = BooleanField('Disable Registration')  
    submit = SubmitField('Save Change')

class AccountForm(FlaskForm):
    start = SubmitField('Start Month')
    salary_deposit = DecimalField('Monthly Salary Deposit', validators=[DataRequired()])
    windfall = DecimalField('Extra funds')
    rent = DecimalField('Rent')
    housekeeping = DecimalField('Houskeeping')
    extra_groceries = DecimalField('Extra Groceries')
    water = DecimalField('Water')
    electric = DecimalField('Electric')
    internet = DecimalField('Internet')
    subscriptions = DecimalField('Subscripions')
    investments = DecimalField('Investments')
    insurance = DecimalField('Insurance')
    counciltax = DecimalField('Council Tax')
    streaming = DecimalField('Streaming')
    family_entertainment = DecimalField('Family Entertainment')
    takeaway = DecimalField('Takeaway')
    transport = DecimalField('Transport')
    fitness = DecimalField('Fitness')
    bakery = DecimalField('Bakery')
    shopping = DecimalField('Shopping')
    workfood = DecimalField('Work Food')
    submit = SubmitField('Rack the Tab')

class WorkfoodForm(FlaskForm):
    work_breakfast = DecimalField('Breakfast Before Work')
    work_lunch = DecimalField('Lunch on Work Days')
    after_work_social = DecimalField('Social Drinks evening')
    work_snacks_me = DecimalField('Snacks Draw')
    work_snacks_share = DecimalField('Snacks Share')
    submit = SubmitField('Update')

class ExtragroceriesForm(FlaskForm):
    extra_groceries_description = TextAreaField('Extra Items', validators=[DataRequired()])
    extra_groceries = DecimalField('Cost')
    submit = SubmitField('Declare Extra')

class SubscriptionsForm(FlaskForm):
    subscription_name = StringField('Subscription', validators=[DataRequired()])
    subscription_term = RadioField('Monthly / Yearly', choices=['Monthly', 'Yearly'], validators=[DataRequired()])
    subscription_start_date = DateTimeField('Subscription Start', format='%d-%m-%y', validators=[DataRequired()])
    subscription_cost = DecimalField('Cost', validators=[DataRequired()])
    submit = SubmitField('Subscribed')

class TransportForm(FlaskForm):
    destination = StringField('Destination', validators=[DataRequired()])
    method_of_travel = RadioField('Method of Travel', choices=['Train', 'Bus', 'Uber', 'Taxi', 'Plane'], validators=[DataRequired()])
    cost_of_travel = DecimalField('Cost of Travel', validators=[DataRequired()])
    submit = SubmitField('On the Move')