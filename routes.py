from cgitb import html
from flask import request, render_template, flash, redirect,url_for
from models import User, Likesdislikes, Thinking, Day_school, People, Admin
from forms import RegistrationForm, LoginForm, LikesDislikesForm, ThinkingForm, DaySchoolForm, GoodBadUglyForm, AdminForm
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from datetime import datetime, timedelta 
  
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
  if request.method == 'GET':

    return render_template('user.html')
	
@app.route('/admin/<username>', methods=['GET', 'POST'])
@login_required
def admin(username):
  admin_form = AdminForm()
  if request.method == 'GET':
    admin = User.query.filter(User.username == username).first()
    print(admin.username, admin.admin)
    confirm_admin = ''
    if admin.admin:
      confirm_admin = True
      return render_template('admin.html', confirm_admin=confirm_admin, admin_form=admin_form)
    else:
      confirm_admin = False
      return render_template('admin.html', confirm_admin=confirm_admin)

  if request.method == 'POST' and admin_form.validate():
    new_adminform = Admin(registration=admin_form.registration.data)
    db.session.add(new_adminform)
    db.session.commit()
    return redirect(url_for('admin', username=current_user.username))



@app.route('/')
def index():
  #by deducting a number of days from the current datetime you have an comparable datetime to compare to the database, we could still run into time issues.
  #We could separate the day, Month, year and time before saving it to separate columns in the database to make it easier to query
  #Until we put in more suphisticated filtering it solves for pulling in the whole table
  new_date = datetime.now() - timedelta(days = 5)
  print(new_date)
  #function route currently not scalable because its calling for all the data in the tables which will grow over time.
  likesdislikes = Likesdislikes.query.filter(Likesdislikes.timestamp > new_date).all()
  #pull one record using the ID
  likesdislikes_id = Likesdislikes.query.get(1)
  #print one property referenced by a foreign key in another class.
  print(likesdislikes_id.username)
  #filtering starts with the model name then .query.filter then the modelname again and the property with logic and all()
  #In this case we filter by the likes only
  likesdislikes_like = Likesdislikes.query.filter(Likesdislikes.likes_dislikes == 'Likes').all()
  print(likesdislikes_like)
  # In this case we filter by id's greater than 1 and save all of them
  likesdislikes_greater = Likesdislikes.query.filter(Likesdislikes.id > 1).all()
  print(likesdislikes_greater)
  # In this case we filter by username which is a field we get through relationship with User and then call all records by a user that are Likes
  likesdislikes_username = Likesdislikes.query.filter(Likesdislikes.username == 'richard', Likesdislikes.likes_dislikes == 'Likes').all()
  print(likesdislikes_username)
  # The first record from a list of records that match the logic specified in this case just the first record.
  people_date = People.query.first()
  #print the year, month, day from a datetime object stored in the database
  print( people_date.date.day, people_date.date.month, people_date.date.year )
  people = People.query.filter(People.date > new_date).all() 

  thoughts = Thinking.query.filter(Thinking.timestamp > new_date).all()

  lucky = Thinking.query.filter(Thinking.thoughts.like('%lucky%')).all()
  for luck in lucky:
    print(luck)

  days = Day_school.query.filter(Day_school.date > new_date).all()
  
  if not likesdislikes:
    likesdislikes=[]
  
#render template returns the html page and passes the data called through to be unpacked on that page
  return render_template( 'landing_page.html', likesdislikes=likesdislikes, thoughts=thoughts, days=days, current_user=current_user, people=people )

@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
  form = ThinkingForm()
  if request.method == 'GET':
    return render_template('survey.html', form=form)

  if request.method == 'POST' and form.validate():
#Thinking is a database class as can be seen if you look at the import statements above and check the models.
    new_thoughts = Thinking(thinking_about = form.thinking_about.data, country=form.country.data, thoughts=form.thoughts.data, username=current_user.username )
#commands to send the new class to the database to persist the data, note the need for the two statements.
    db.session.add(new_thoughts)
    db.session.commit()
#A redirect statement to the index function/route showing that the view is changing after the render.
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

@app.route('/likesdislikes', methods=['GET', 'POST'])
def likesdislikes():
  form = LikesDislikesForm()
  if request.method == 'GET':
    user = current_user
    user = User.query.filter_by(username=user.username).first()
    print(user.username)
    likesdislikes = Likesdislikes.query.filter_by(username=user.username)
    for likedislike in likesdislikes:
      print(likedislike)
    
    return render_template('likesdislikes.html', likesdislikes=likesdislikes, form=form)
  
  if request.method == 'POST':
    print('Hello World')
    new_likesdislikes = Likesdislikes(likes_dislikes=form.likes_dislikes.data, country=form.country.data, reason=form.reason.data, username=current_user.username)
    db.session.add(new_likesdislikes)
    db.session.commit()

    return redirect(url_for('index'))
    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))