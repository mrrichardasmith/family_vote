from wsgiref import validate
from flask import request, render_template, flash, redirect, url_for
from models import User, Likesdislikes, Thinking, Day_school, People, Admin, Life_hacks, Account, Workfood, Extragroceries, Subscriptions, Transport, Familyentertainment, Takeaway, Insurance, Investments
from forms import RegistrationForm, LoginForm, LikesDislikesForm, ThinkingForm, DaySchoolForm, GoodBadUglyForm, AdminForm, LifeHacksForm, AccountForm, WorkfoodForm, ExtragroceriesForm, SubscriptionsForm, TransportForm, FamilyentertainmentForm, TakeawayForm, InvestmentsForm, InsuranceForm
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from datetime import datetime, timedelta 
from helper import month_from_number

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
    registration = Admin.query.first()      
    return render_template('login.html', title='Sign In', form=form, registration=registration)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
      return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    email=form.email.data)
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

    return render_template('user.html', username=username)
	
@app.route('/admin/<username>', methods=['GET', 'POST'])
@login_required
def admin(username):
  admin_form = AdminForm()
  
  if request.method == 'GET':
    admin = User.query.filter(User.username == username).first()
    registration = Admin.query.first()
    if registration != None:
      print(registration.registration)
      print(admin.username, admin.admin)
    
    
    if admin.admin == 'admin':
      
      return render_template('admin.html', admin=admin, admin_form=admin_form, registration=registration)

    else:
      print('Supressed Registration Page')
      confirm_admin = False
      return render_template('admin.html', confirm_admin=confirm_admin, admin=admin)

  if request.method == 'POST' and admin_form.validate():
    
    new_admin = Admin.query.get(1)
    print(new_admin)
    if new_admin.registration == True:
      new_admin.registration = False
    else:
      new_admin.registration = True
    db.session.commit()
    return redirect(url_for('admin', username=current_user.username))

@app.route('/')
def index():
  #by deducting a number of days from the current datetime you have an comparable datetime to compare to the database, we could still run into time issues.
  #We could separate the day, Month, year and time before saving it to separate columns in the database to make it easier to query
  #Until we put in more suphisticated filtering it solves for pulling in the whole table
  new_date = datetime.now() - timedelta(days = 7)
  print(new_date)
  #function route currently not scalable because its calling for all the data in the tables which will grow over time.
  likesdislikes = Likesdislikes.query.filter(Likesdislikes.timestamp > new_date).all()
  #pull one record using the ID
  likesdislikes_id = Likesdislikes.query.get(2)

  #print one property referenced by a foreign key in another class.
  print(likesdislikes_id.reason)
  #filtering starts with the model name then .query.filter then the modelname again and the property with logic and all()
  #In this case we filter by the likes only
  likesdislikes_like = Likesdislikes.query.filter(Likesdislikes.likes_dislikes == 'Likes').all()
  #print(likesdislikes_like)
  # In this case we filter by id's greater than 1 and save all of them
  likesdislikes_greater = Likesdislikes.query.filter(Likesdislikes.id > 1).all()
  #print(likesdislikes_greater)
  # In this case we filter by username which is a field we get through relationship with User and then call all records by a user that are Likes
  likesdislikes_username = Likesdislikes.query.filter(Likesdislikes.username == 'richard', Likesdislikes.likes_dislikes == 'Likes').all()
  #print(likesdislikes_username)

  days = Day_school.query.filter(Day_school.date > new_date).all()
  
  if not likesdislikes:
    likesdislikes=[]
  
#render template returns the html page and passes the data called through to be unpacked on that page
  return render_template( 'landing_page.html', current_user=current_user )

@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
  form = ThinkingForm()
  if request.method == 'GET':
    return render_template('survey.html', form=form)

  if request.method == 'POST' and form.validate():
#Thinking is a database class as can be seen if you look at the import statements above and check the models.
    new_thoughts = Thinking(thinking_about = form.thinking_about.data, 
                            thoughts=form.thoughts.data, 
                            username=current_user.username )
#commands to send the new class to the database to persist the data, note the need for the two statements.
    db.session.add(new_thoughts)
    db.session.commit()
#A redirect statement to the index function/route showing that the view is changing after the render.
    return redirect(url_for('likesdislikes'))

@app.route('/day',  methods=['GET', 'POST'])
@login_required
def day():
  dayform = DaySchoolForm()
  if request.method == 'GET':
    return render_template('day_school.html', dayform=dayform)

  if request.method == 'POST' and dayform.validate():
    new_day = Day_school(yourday=dayform.yourday.data, 
                         why=dayform.why.data, 
                         username=current_user.username)

    db.session.add(new_day)
    db.session.commit()
    return redirect(url_for('people'))

@app.route('/people', methods=['GET', 'POST'])
@login_required
def people():
  new_people = GoodBadUglyForm()
  if request.method == 'GET':
    return render_template('people.html', peopleForm=new_people)

  if request.method == 'POST' and new_people.validate():
    new_people = People(good=new_people.good.data, 
                        bad=new_people.bad.data, 
                        ugly=new_people.ugly.data, 
                        morewords=new_people.morewords.data, 
                        username=current_user.username)

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

@app.route('/lifehacks', methods=['GET', 'POST'])
@login_required
def lifehacks():
  hack = LifeHacksForm()
  if  request.method == 'GET':
    

    return render_template('lifehacks.html', user=current_user, hack=hack)

  if request.method == 'POST' and hack.validate():
    print('Family Hacks')
    new_hack = Life_hacks(hacktitle=hack.hack_title.data, 
                          hackdescription=hack.hack_description.data, 
                          username=current_user.username)
    
    db.session.add(new_hack)
    db.session.commit()
    return redirect(url_for('lifehacks'))
    
@app.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():

  account = AccountForm()
  todayDate = datetime.now()
  active = Account.query.filter(Account.username == current_user.username
                                and Account.month == todayDate.month 
                                and Account.year == todayDate.year).first()

  if  request.method == 'GET':
    print(todayDate.month)
    
    total = 0
    remaining = 0
    current_month = month_from_number(todayDate.month)

    current_food = Workfood.query.filter(Workfood.username == current_user.username
                                         and Workfood.month == todayDate.month
                                         and Workfood.year == todayDate.year).all()

    workfood_total = 0
    if current_food != None:
      for sum in current_food:
        workfood_total += sum.sum_food
     

    extra_groceries = Extragroceries.query.filter(Extragroceries.username == current_user.username
                                                  and Extragroceries.month == todayDate.month 
                                                  and Extragroceries.year == todayDate.year).all()
    
    extra_groceries_total = 0
    if extra_groceries != None:
      for extra in extra_groceries:
        extra_groceries_total += extra.costgroceries

    transport = Transport.query.filter(Transport.username == current_user.username
                                       and Transport.month == todayDate.month 
                                       and Transport.year == todayDate.year).all()

    total_transport = 0
    if transport != None:
      for t in transport:
        total_transport += t.cost_of_travel
    
    subscriptions = Subscriptions.query.filter(Subscriptions.username == current_user.username
                                               and Subscriptions.month == todayDate.month
                                               and Subscriptions.year == todayDate.year).all()

    total_subscriptions = 0
    if subscriptions != None:
      for s in subscriptions:
        total_subscriptions += s.subscription_cost

    investments = Investments.query.filter(Investments.username == current_user.username and Investments.month == todayDate.month and Investments.year == todayDate.year).all()
    
    total_investments = 0
    if investments != None:
      for i in investments:
        total_investments += i.investment_cost

    insurance = Insurance.query.filter(Insurance.username == current_user.username and Insurance.month == todayDate.month and Insurance.year == todayDate.year).all()

    total_insurance = 0
    if insurance != None:
      for i in insurance:
        total_insurance += i.insurance_cost
    

    family_entertainment = Familyentertainment.query.filter(Familyentertainment.username == current_user.username
                                                            and Subscriptions.month == todayDate.month
                                                            and Subscriptions.year == todayDate.year).all()

    total_entertainment = 0
    if family_entertainment != None:
      for family in family_entertainment:
        total_entertainment += family.entertainment_cost
    

    takeaways = Takeaway.query.filter(Takeaway.username == current_user.username
                                      and Subscriptions.month == todayDate.month
                                      and Subscriptions.year == todayDate.year).all()
    
    total_takeaway = 0
    if takeaways != None:
      for take in takeaways:
        total_takeaway += take.takeaway_cost

    if active != None and active.rent != None:
      total += active.rent 
    if active != None and active.housekeeping != None:
      total += active.housekeeping
    if extra_groceries_total > 0:
      total += extra_groceries_total
    if active != None and active.water != None:
      total += active.water
    if active != None and active.electric != None:
      total += active.electric
    if active != None and active.internet != None:
      total += active.internet
    if total_subscriptions > 0:
      total += total_subscriptions
    if total_investments > 0:
      total += total_investments
    if total_insurance > 0:
      total += total_insurance
    if active != None and active.counciltax != None:
      total += active.counciltax
    if active != None and active.streaming != None:
      total += active.streaming
    if total_entertainment > 0:
      total += total_entertainment
    if total_takeaway > 0:
      total += total_takeaway
    if total_transport > 0:
      total += total_transport
    if active != None and active.fitness != None:
      total += active.fitness
    if active != None and active.bakery != None:
      total += active.bakery  
    if active != None and active.shopping != None:
      total += active.shopping  
    if workfood_total > 0:
      total += workfood_total
    if active != None and active.salary_deposit != None:
      remaining = active.salary_deposit - total
    if active != None and active.windfall != None:
      remaining = remaining + active.windfall 
      


    remaining_formatted = '{:.2f}'.format(remaining)
    print(remaining_formatted)

    return render_template('accounts.html', 
                           user=current_user,
                           current_month=current_month, 
                           account=account, 
                           active=active, 
                           remaining=remaining, 
                           workfood_total=workfood_total,
                           extra_groceries_total=extra_groceries_total,
                           total_transport=total_transport,
                           total_subscriptions=total_subscriptions,
                           total_investments=total_investments,
                           total_insurance=total_insurance,
                           total_entertainment=total_entertainment,
                           total_takeaway=total_takeaway)

  if request.method == 'POST': 
    
    if active == None:
      new_account = Account(month=todayDate.month, 
                            year=todayDate.year, 
                            salary_deposit=account.salary_deposit.data, 
                            windfall=account.windfall.data, 
                            rent=account.rent.data,
                            rent_lock=account.rent_lock.data,  
                            housekeeping=account.housekeeping.data,  
                            water=account.water.data,
                            water_lock = account.water_lock.data,
                            electric=account.electric.data,
                            electric_lock=account.electric_lock.data, 
                            internet=account.internet.data,
                            internet_lock=account.internet_lock.data,
                            investments=account.investments.data,
                            insurance=account.insurance.data, 
                            counciltax=account.counciltax.data,
                            counciltax_lock=account.counciltax_lock.data,
                            streaming=account.streaming.data, 
                            fitness=account.fitness.data, 
                            bakery=account.bakery.data, 
                            shopping=account.shopping.data,  
                            username=current_user.username )
      db.session.add(new_account)  

    if active != None and active.salary_deposit == None:
       active.salary_deposit = account.salary_deposit.data

    if active != None and active.windfall == None:
       active.windfall = account.windfall.data

    if active != None and active.rent == None:
       active.rent = account.rent.data

    if active != None and active.rent_lock != None:
      active.rent_lock=account.rent_lock.data
        
    if active != None and active.housekeeping == None:
      active.housekeeping=account.housekeeping.data

    if active != None and active.water == None:
      active.water=account.water.data

    if active != None and active.water_lock != None:
      active.water_lock=account.water_lock.data

    if active != None and active.electric == None:
      active.electric=account.electric.data

    if active != None and active.electric_lock != None:
      active.electric_lock=account.electric_lock.data

    if active != None and active.internet == None:
      active.internet=account.internet.data

    if active != None and active.internet_lock != None:
      active.internet_lock=account.internet_lock.data 

    if active != None and active.investments == None:
      active.investments=account.investments.data
    
    if active != None and active.insurance == None:
      active.insurance=account.insurance.data

    if active != None and active.counciltax == None:
      active.counciltax = account.counciltax.data

    if active != None and active.counciltax != None and active.counciltax_lock != None:
      active.counciltax_lock=account.counciltax_lock.data

#First line looks to see if the Database is empty to avoid the None error of an empty object
#In the case the database is empty we start by assigning the same value to the previous as the current lock setting
#Above we also validate that a value is passed to the counciltax input before setting the lock setting
#Then we watch the settings change when the current setting changes the first time we do nothing
#Instead we wait until the form value becomes the same as the previous setting and then we know its time to change
#the previous setting to the alternate boolean.
    if active != None and active.counciltax != None and active.counciltax_lock_previous == None:
      active.counciltax_lock_previous=account.counciltax_lock.data
    elif active != None and active.counciltax != None and active.counciltax_lock_previous != None:
      if account.counciltax_lock.data == active.counciltax_lock_previous:
        active.counciltax_lock_previous = not active.counciltax_lock_previous
        
      
      
    if active != None and active.streaming == None:
      active.streaming = account.streaming.data

    if active != None and active.fitness == None:
      active.fitness = account.fitness.data

    if active != None and active.bakery == None:
      active.bakery = account.bakery.data
    
    if active != None and active.shopping == None:
      active.shopping = account.shopping.data

    db.session.commit()  
    return redirect(url_for('accounts'))

@app.route('/workfood', methods=['GET', 'POST'])
@login_required
def workfood():
  foodform = WorkfoodForm()
  todayDate = datetime.now()  
  
  if request.method == 'GET':
    sum_breakfast = 0
    sum_lunch = 0
    sum_social = 0
    sum_snacks_me = 0
    sum_snacks_share = 0

    current_food = Workfood.query.filter(Workfood.username == current_user.username
                                         and Workfood.month == todayDate.month
                                         and Workfood.year == todayDate.year).all()

    grand_total = 0
    if current_food != None:
      for sum in current_food:
        grand_total += sum.sum_food
      print(grand_total)
  
    
    for food in current_food:
      if food.work_breakfast != None:
        sum_breakfast += food.work_breakfast
      if food.work_lunch != None:
        sum_lunch += food.work_lunch
      if food.after_work_social != None:
        sum_social += food.after_work_social
      if food.work_snacks_me != None:
        sum_snacks_me += food.work_snacks_me
      if food.work_snacks_share != None:
        sum_snacks_share += food.work_snacks_share


    return render_template('workfood.html', 
                            foodform=foodform, 
                            current_food=current_food, 
                            sum_breakfast=sum_breakfast,
                            sum_lunch=sum_lunch,
                            sum_social=sum_social,
                            sum_snacks_me=sum_snacks_me,
                            sum_snacks_share=sum_snacks_share,
                            grand_total=grand_total)

  if request.method == 'POST' and foodform.validate():
    sum_food = 0

    if foodform.work_breakfast.data != None:
      sum_food += foodform.work_breakfast.data
    if foodform.work_lunch.data != None:
      sum_food += foodform.work_lunch.data
    if foodform.after_work_social.data != None:
      sum_food += foodform.after_work_social.data
    if foodform.work_snacks_me.data != None:
      sum_food += foodform.work_snacks_me.data
    if foodform.work_snacks_share.data != None:
      sum_food += foodform.work_snacks_share.data

    print(sum_food) 
    new_workfood = Workfood(day=todayDate.day,
                            month=todayDate.month, 
                            year=todayDate.year, 
                            work_breakfast=foodform.work_breakfast.data, 
                            work_lunch=foodform.work_lunch.data, 
                            after_work_social=foodform.after_work_social.data, 
                            work_snacks_me=foodform.work_snacks_me.data, 
                            work_snacks_share=foodform.work_snacks_share.data,
                            username=current_user.username,
                            sum_food=sum_food)

    db.session.add(new_workfood)
    db.session.commit()



    return redirect(url_for('workfood')) 

@app.route('/likesdislikes', methods=['GET', 'POST'])
@login_required
def likesdislikes():
  form = LikesDislikesForm()
  if request.method == 'GET':
    user = current_user
    user = User.query.filter_by(username=user.username).first()
    likesdislikes = Likesdislikes.query.filter_by(username=user.username)
    
    
    return render_template('likesdislikes.html', likesdislikes=likesdislikes, form=form)
  
  if request.method == 'POST' and form.validate():
    print('Likes & Dislikes POST')
    new_likesdislikes = Likesdislikes(likes_dislikes=form.likes_dislikes.data, 
                                      country=form.country.data, 
                                      reason=form.reason.data, 
                                      username=current_user.username)
    
    db.session.add(new_likesdislikes)
    db.session.commit()

    return redirect(url_for('index'))
    
@app.route('/subscriptions', methods=['GET', 'POST'])
def subscriptions():
  subs = SubscriptionsForm()
  if request.method == 'GET':

    current_subscriptions = Subscriptions.query.filter(Subscriptions.username == current_user.username).all()

    return render_template('subscriptions.html', subs=subs, current_subscriptions=current_subscriptions)

  if request.method == 'POST' and subs.validate():
    new_subscriptions = Subscriptions(subscription_name=subs.subscription_name.data,
                                      subscription_term=subs.subscription_term.data,
                                      subscription_start_date=subs.subscription_start_date.data,
                                      subscription_cost=subs.subscription_cost.data,
                                      username=current_user.username)

    db.session.add(new_subscriptions)
    db.session.commit()

    return redirect(url_for('accounts'))

@app.route('/investments', methods=['GET', 'POST'])
def investments():
  todayDate = datetime.now()
  inv = InvestmentsForm()
  if request.method == 'GET':

    current_investments = Investments.query.filter(Investments.username == current_user.username, Investments.month == todayDate.month, Investments.year == todayDate.year).all()
    
    return render_template('investments.html', inv=inv, current_investments=current_investments)

  if request.method == 'POST' and inv.validate():
  
    new_investments = Investments(day=todayDate.day,
                                  month=todayDate.month,
                                  year=todayDate.year,
                                  investment_name=inv.investment_name.data,
                                  investment_description=inv.investment_description.data,
                                  investment_cost=inv.investment_cost.data,
                                  username=current_user.username)
    db.session.add(new_investments)
    db.session.commit()
    return redirect(url_for('investments'))

@app.route('/insurance', methods=['GET', 'POST'])
def insurance():
  todayDate = datetime.now()
  ins = InsuranceForm()
    
  if request.method == 'GET':
    current_insurance = Insurance.query.filter(Insurance.username == current_user.username and Insurance.month == todayDate.month).all()  
    
    return render_template('insurance.html', ins=ins, current_insurance=current_insurance)
  
  if request.method == 'POST' and ins.validate():

    new_insurance = Insurance(day=todayDate.day,
                              month=todayDate.month,
                              year=todayDate.year,
                              insurance_name=ins.insurance_name.data,
                              insurance_description=ins.insurance_description.data,
                              insurance_cost=ins.insurance_cost.data,
                              username=current_user.username)

    db.session.add(new_insurance)
    db.session.commit()
    return redirect(url_for('insurance'))


@app.route('/extra_groceries', methods=['GET', 'POST'])
@login_required
def extragroceries():
  todayDate = datetime.now()
  extra = ExtragroceriesForm()
  monthNow = month_from_number(todayDate.month)

  if request.method == 'GET':
    
    extra_groceries = Extragroceries.query.filter(Extragroceries.username == current_user.username
                                                  and Extragroceries.month == todayDate.month 
                                                  and Extragroceries.year == todayDate.year).all()

    list = []
    for l in extra_groceries:
      space = l.grocerydescription.split(' ')
      print(space)
      for s in space:
        list.append(s)
      for a in list:
        print(a)
  
    
    return render_template('extragroceries.html', extra=extra, list=list, monthNow=monthNow)

  if request.method == 'POST' and extra.validate():
    print('We have extra groceries')
    new_groceries = Extragroceries(day=todayDate.day,
                                   month=todayDate.month, 
                                   year=todayDate.year,
                                   grocerydescription=extra.extra_groceries_description.data,
                                   costgroceries=extra.extra_groceries.data,
                                   username=current_user.username) 

    db.session.add(new_groceries)
    db.session.commit()

    return redirect(url_for('extragroceries'))

@app.route('/transport', methods=['GET', 'POST'])
@login_required
def transport():
  transp = TransportForm()
  todayDate = datetime.now()
  current_month = month_from_number(todayDate.month)
  if request.method == 'GET':
    total_train = 0
    total_bus = 0
    total_uber = 0
    total_taxi = 0
    total_plane = 0
    method_totals = []

    get_transp = Transport.query.filter(Transport.username == current_user.username 
                                        and Transport.date.month==todayDate.month).all()
    

    if get_transp != None:
      for method in get_transp:
        if method.method_of_travel == 'Train':
          total_train += method.cost_of_travel
        elif method.method_of_travel == 'Bus':
          total_bus += method.cost_of_travel
        elif method.method_of_travel == 'Uber':
          total_uber += method.cost_of_travel
        elif method.method_of_travel == 'Taxi':
          total_taxi += method.cost_of_travel
        elif method.method_of_travel == 'Plane':
          total_plane += method.cost_of_travel

    method_totals.append(total_train)
    method_totals.append(total_bus) 
    method_totals.append(total_uber) 
    method_totals.append(total_taxi)
    method_totals.append(total_plane)
    print(method_totals)

    transport_methods = ['Train', 'Bus', 'Uber', 'Taxi', 'Plane']
    
    
    return render_template('transport.html', transp=transp, current_month=current_month, transport_methods=transport_methods, method_totals=method_totals)

  if request.method == 'POST' and transp.validate():

    new_transport = Transport(destination=transp.destination.data,
                              method_of_travel=transp.method_of_travel.data,
                              cost_of_travel=transp.cost_of_travel.data,
                              username=current_user.username
                              )

    db.session.add(new_transport)
    db.session.commit()

    return redirect(url_for('accounts'))

@app.route('/familyentertainment', methods=['GET', 'POST'])
@login_required
def familyentertainment():
  FamilyentForm = FamilyentertainmentForm()
  todayDate = datetime.now()
  if request.method == 'GET':

    return render_template('familyentertainment.html', FamilyentForm = FamilyentForm)
  
  if request.method == 'POST' and FamilyentForm.validate():
    new_entertainment = Familyentertainment(day=todayDate.day, 
                                            month=todayDate.month, 
                                            year=todayDate.year, 
                                            entertainment_title=FamilyentForm.entertainment_title.data,
                                            entertainmnet_description=FamilyentForm.entertainment_description.data,
                                            entertainment_cost=FamilyentForm.entertainment_cost.data,
                                            username = current_user.username)
    db.session.add(new_entertainment)
    db.session.commit()
    return redirect(url_for('accounts'))

@app.route('/takeaway', methods=['GET', 'POST'])
@login_required
def takeaway():
  todayDate = datetime.now()
  takeaway = TakeawayForm()
  if request.method == 'GET':

    return render_template('takeaway.html', takeaway=takeaway)

  if request.method == 'POST' and takeaway.validate():

    new_takeaway = Takeaway(username=current_user.username,
                            day=todayDate.day,
                            month=todayDate.month,
                            year=todayDate.year,
                            takeaway_choice=takeaway.takeaway_choice.data,
                            takeaway_other=takeaway.takeaway_other.data,
                            takeaway_cost=takeaway.takeaway_cost.data)

    db.session.add(new_takeaway)
    db.session.commit()
    return redirect(url_for('accounts'))

@app.route('/reports')
@login_required
def reports():
  if request.method == 'GET':
    
    return render_template('reports.html')

@app.route('/pulse_report')
@login_required
def pulsereport():
  if request.method == 'GET':
    new_date = datetime.now() - timedelta(days = 30)
    days = Day_school.query.filter(Day_school.date > new_date).all()
    return render_template('familypulsereport.html', days=days, testdelete=testdelete)

@app.route('/likesdislikes_report')
@login_required
def likesdislikesreport():
  if request.method == 'GET':
    new_date = datetime.now() - timedelta(days = 30)
    likesdislikes = Likesdislikes.query.filter(Likesdislikes.timestamp > new_date).all()
    return render_template('likesdislikesreport.html', likesdislikes=likesdislikes)

@app.route('/people_report')
@login_required
def peoplereport():
  if request.method == 'GET':
    new_date = datetime.now() - timedelta(days = 30)
    print(new_date)
    people = People.query.filter(People.date > new_date).all()
    # The first record from a list of records that match the logic specified in this case just the first record.
    people_date = People.query.first()
    #print the year, month, day from a datetime object stored in the database
    #print( people_date.date.day, people_date.date.month, people_date.date.year )
    return render_template('peoplereport.html', people=people)

@app.route('/thoughts_report')
@login_required
def thoughtreport():
  if request.method == 'GET':
    new_date = datetime.now() - timedelta(days = 30)
    print(new_date)
    thoughts = Thinking.query.filter(Thinking.timestamp > new_date).all()
    return render_template('thoughtsreport.html', thoughts=thoughts)

@app.route('/lifehacks_report')
@login_required
def lifehacksreport():
  if request.method == 'GET':
    new_date = datetime.now() - timedelta(days = 30)
    print(new_date)
    hacks = Life_hacks.query.filter(Life_hacks.date > new_date).all()
    
    return render_template('lifehacks_report.html', hacks=hacks)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def testdelete(id):
  print('Function Fired')
  delete = Day_school.query.filter(Day_school.id == id).first()
  db.session.delete(delete)
  db.session.commit()
    
  return 'This is a test delete route'

@app.route('/testupdate/<id>/<yourday>', methods=['GET', 'POST'])
def testupdate(id, yourday):
  if request.method == 'GET':
    update = Day_school.query.get(id)
    update.yourday = yourday
    db.session.commit()

  return 'This is a test update'





    
  
