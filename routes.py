from flask import request, render_template, flash, redirect,url_for
from models import User, Post, Thinking, Day_school, People
from forms import RegistrationForm, LoginForm, DestinationForm, ThinkingForm, DaySchoolForm, GoodBadUglyForm
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db 
  
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
      return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
  #user = current_user
	user = User.query.filter_by(username=user.username).first()
	posts = Post.query.filter_by(username=user.username)
	if posts is None:
		posts = []
	form = DestinationForm()
	if request.method == 'POST' and form.validate():
		new_studying = Post(likesDislikes=form.likesDislikes.data,country=form.country.data,reason=form.reason.data, username=user.username)
		db.session.add(new_studying)
		db.session.commit()
	else:
		flash(form.errors)
  
	return render_template('user.html', user=user, posts=posts, form=form)


@app.route('/')
def index():
  posts = Post.query.all()
  thoughts = Thinking.query.all()
  days = Day_school.query.all()
  people = People.query.all()
  if not posts:
    posts=[]
  return render_template( 'landing_page.html', posts=posts, thoughts=thoughts, days=days, current_user=current_user, people=people )

@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
  form = ThinkingForm()
  if request.method == 'GET':
    return render_template('survey.html', form=form)

  if request.method == 'POST' and form.validate():
    new_thoughts = Thinking(thinking_about = form.thinking_about.data, country=form.country.data, thoughts=form.thoughts.data, username=current_user.username )
    db.session.add(new_thoughts)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/day',  methods=['GET', 'POST'])
@login_required
def day():
  dayform = DaySchoolForm()
  if request.method == 'GET':
    return render_template('day_school.html', dayform=dayform)

  if request.method == 'POST' and dayform.validate():
    new_day = Day_school( yourday = dayform.yourday.data, why=dayform.why.data, username=current_user.username )
    db.session.add(new_day)
    db.session.commit()
    return redirect(url_for('people'))

@app.route('/people', methods=['GET', 'POST'])
def people():
  new_people = GoodBadUglyForm()
  if request.method == 'GET':
    return render_template('people.html', peopleForm=new_people)

  if request.method == 'POST' and new_people.validate():
    new_people = People(good=new_people.good.data, bad=new_people.bad.data, ugly=new_people.ugly.data, morewords=new_people.morewords.data, username=current_user.username)
    db.session.add(new_people)
    db.session.commit()
    return redirect(url_for('survey'))

@app.route('/food', methods=['GET', 'POST'])
def food():
  if request.method == 'GET':
    return render_template('foods.html')

@app.route('/faces', methods=['GET', 'POST'])
def faces  ():
  if request.method == 'GET':
    return render_template('faces.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))