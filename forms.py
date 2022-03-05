from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateTimeField, RadioField
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

class DestinationForm(FlaskForm):
    studying = StringField('studying')
    country = StringField('country')
    description = StringField('description')
    submit = SubmitField('Post')

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
    country = SelectField(u'Country', choices=[('USA', 'United States'), ('UK', 'United Kingdom'), ('EU', 'Europe')])
    thoughts = StringField('Your thoughts', validators=[DataRequired()])
    submit = SubmitField('Say It')

class DaySchoolForm(FlaskForm):
    yourday = RadioField('Your Day Was', choices=['Great', 'OK', 'Blah', 'Ugh!', 'Bad'], validators=[DataRequired()])
    why = StringField('One Word Why', validators=[DataRequired()])
    submit = SubmitField('Day Done')
    

