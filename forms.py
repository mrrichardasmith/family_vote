from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, RadioField, TextAreaField, DecimalField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class LikesDislikesForm(FlaskForm):
    likes_dislikes = RadioField('Like or Dislike', choices=['Likes', 'Dislikes'], validators=[DataRequired()])
    country = SelectField(u'Country', choices=[('USA', 'United States'), ('UK', 'United Kingdom'), ('EU', 'Europe')])
    reason = StringField('More Words', validators=[DataRequired()])
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
    registration = BooleanField('Enable Registration')  
    submit = SubmitField('Save Change')

class AccountForm(FlaskForm):
    start = SubmitField('Start Month')
    salary_deposit = DecimalField('Monthly Salary Deposit', validators=[DataRequired()])
    windfall = DecimalField('Extra funds')
    rent = DecimalField('Rent')
    rent_lock = BooleanField('Lock Rent')
    housekeeping = DecimalField('Houskeeping')
    water = DecimalField('Water')
    water_lock = BooleanField('Lock Water')
    electric = DecimalField('Electric')
    electric_lock = BooleanField('Lock Electric')
    internet = DecimalField('Internet')
    internet_lock = BooleanField('Lock Cost')
    investments = DecimalField('Investments')
    insurance = DecimalField('Insurance')
    counciltax = DecimalField('Council Tax')
    counciltax_lock = BooleanField('Lock Council Tax')
    streaming = DecimalField('Streaming')
    fitness = DecimalField('Fitness')
    bakery = DecimalField('Bakery')
    shopping_total = DecimalField('Shopping')
    submit = SubmitField('Update')

class WorkfoodForm(FlaskForm):
    work_breakfast = DecimalField('Breakfast Before Work')
    work_lunch = DecimalField('Lunch on Work Days')
    after_work_social = DecimalField('Social Drinks evening')
    work_snacks_me = DecimalField('Snacks Draw')
    work_snacks_share = DecimalField('Snacks Share')
    submit = SubmitField('Update')

class ExtragroceriesForm(FlaskForm):
    extra_groceries_description = StringField('Extra Items', validators=[DataRequired()])
    extra_groceries = DecimalField('Cost', validators=[DataRequired()])
    submit = SubmitField('Declare Extra')

class StuffForm(FlaskForm):
    description = TextAreaField('Line Item Detail:', validators=[DataRequired()])
    cost = DecimalField('Item or Total Cost')
    submit = SubmitField('Purchased')

class SubscriptionsForm(FlaskForm):
    subscription_name = StringField('Subscription', validators=[DataRequired()])
    subscription_term = RadioField('Monthly / Yearly', choices=['Monthly', 'Yearly'], validators=[DataRequired()])
    subscription_start_date = DateField('Subscription Start', format='%Y-%m-%d', validators=[DataRequired()])
    cost = DecimalField('Cost', validators=[DataRequired()])
    submit = SubmitField('Subscribed')
    
class FamilyentertainmentForm(FlaskForm):
    entertainment_title = StringField('Entertainment Title', validators=[DataRequired()])
    entertainment_description = TextAreaField('Describe Adventure', validators=[DataRequired()])
    cost = DecimalField('Cost', validators=[DataRequired()])
    submit = SubmitField('Entertained')

class TransportForm(FlaskForm):
    destination = StringField('Destination', validators=[DataRequired()])
    method_of_travel = RadioField('Method of Travel', choices=['Train', 'Bus', 'Uber', 'Taxi', 'Plane'], validators=[DataRequired()])
    cost_of_travel = DecimalField('Cost of Travel', validators=[DataRequired()])
    submit = SubmitField('On the Move')

class TakeawayForm(FlaskForm):
    takeaway_choice = RadioField('Takeaway', choices=['Chinese', 'Indian', 'Kebab', 'Burgers', 'Pizza', 'Other'], validators=[DataRequired()])    
    takeaway_other = StringField('Other Takeaway')
    takeaway_cost = DecimalField('Takeaway Cost', validators=[DataRequired()])
    submit = SubmitField('Take Out')

class InvestmentsForm(FlaskForm):
    investment_name = StringField('Investment Name', validators=[DataRequired()])
    investment_description = TextAreaField('Investment Description', validators=[DataRequired()])
    investment_cost = DecimalField('Investment Cost', validators=[DataRequired()])
    submit = SubmitField('Invest in the Future')

class InsuranceForm(FlaskForm):
    insurance_name = StringField('Insurance Name', validators=[DataRequired()])
    insurance_description = TextAreaField('Type', validators=[DataRequired()])
    insurance_cost = DecimalField('Cost', validators=[DataRequired()])
    submit = SubmitField('Mitigate Risk')

class HousekeepingForm(FlaskForm):
    lineitem_description = StringField('Line Item Description', validators=[DataRequired()])
    lineitem_category = SelectField(u'Cost Category', choices=['Necessary', 'Important', 'Needed', 'Wanted', 'Impulse Buy', 'Revenge Spending'], validators=[DataRequired()])
    cost = DecimalField('Cost', validators=[DataRequired()])
    submit = SubmitField('Housekeeping')