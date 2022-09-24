from flask import request, render_template, flash, redirect, url_for
from models import Credits, User, Likesdislikes, Thinking, Day_school, People, Admin, Life_hacks, Account, Workfood, Extragroceries, Subscriptions, Transport, Familyentertainment, Takeaway, Insurance, Investments, Rollover
from forms import RegistrationForm, LoginForm, LikesDislikesForm, ThinkingForm, DaySchoolForm, GoodBadUglyForm, AdminForm, LifeHacksForm, AccountForm, WorkfoodForm, ExtragroceriesForm, SubscriptionsForm, TransportForm, FamilyentertainmentForm, TakeawayForm, InvestmentsForm, InsuranceForm
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from datetime import datetime, timedelta, date
from helper import find_zero_balance, month_from_number, check_if_float_onerow, total_floats, sum_combined_totals, sum_query_cost
import calendar

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
  
  #function route currently not scalable because its calling for all the data in the tables which will grow over time.
  likesdislikes = Likesdislikes.query.filter(Likesdislikes.timestamp > new_date).all()
  #pull one record using the ID
  likesdislikes_id = Likesdislikes.query.get(2)

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
  current_month_text = month_from_number(todayDate.month)
  
  print(f"{todayDate:%d %B, %Y}")

  active = Account.query.filter(Account.month == todayDate.month
                            and Account.year == todayDate.year 
                            and Account.username == current_user.username).first()

  debit_check = check_if_float_onerow(active)
  debit_total = (total_floats(debit_check))
  
  credits = Credits.query.filter(Credits.month == todayDate.month
                             and Credits.year == todayDate.year
                             and Credits.username == current_user.username).first()

  credit_check = check_if_float_onerow(credits)
  credit_total_single_values = total_floats(credit_check)


  rollover = Rollover.query.filter(Rollover.year == todayDate.year
                               and Rollover.username == current_user.username).first()

  if  request.method == 'GET':

    if active == None:
        new_account = Account(month=todayDate.month, 
                              year=todayDate.year,   
                              rent = 0.0,  
                              housekeeping = 0.0,  
                              water = 0.0,
                              electric = 0.0, 
                              internet = 0.0, 
                              counciltax = 0.0, 
                              fitness = 0.0, 
                              bakery = 0.0, 
                              shopping = 0.0,  
                              username=current_user.username)
        print(vars(new_account))
        db.session.add(new_account)
    

    if credits == None:
        credits = Credits(month=todayDate.month,
                          year=todayDate.year,
                          salary_deposit = 0.0,
                          windfall = 0.0)
        db.session.add(credits)
    

    if rollover == None:
        rollover = Rollover(day=todayDate.day,
                            month=todayDate.month,
                            year=todayDate.year,
                            rent_fixed = 0,
                            rent_lock_previous = False,
                            rent_lock = False,
                            water_fixed = 0,
                            water_lock_previous = False,
                            water_lock = False,
                            electric_fixed = 0,
                            electric_lock_previous = False,
                            electric_lock = False,
                            counciltax_fixed = 0,
                            counciltax_lock_previous = False,
                            counciltax_lock = False,
                            internet_fixed = 0,
                            internet_lock_previous = False,
                            internet_lock = False,
                            username=current_user.username)
    db.session.add(rollover)
    db.session.commit()

  
    current_month_text = month_from_number(todayDate.month)


    extra_groceries = Extragroceries.query.filter(Extragroceries.month == todayDate.month
                                                  and Extragroceries.year == todayDate.year
                                                  and Extragroceries.username == current_user.username).all()

    extra_groceries_total = sum_query_cost(extra_groceries)    
    

    transport = Transport.query.filter(Transport.month == todayDate.month
                                       and Transport.year == todayDate.year
                                       and Transport.username == current_user.username).all()

    total_transport = sum_query_cost(transport)
    
    
    subscriptions = Subscriptions.query.filter(Subscriptions.month == todayDate.month
                                           and Subscriptions.year == todayDate.year
                                           and Subscriptions.username == current_user.username).all()

    total_subscriptions = sum_query_cost(subscriptions)
    

    investments = Investments.query.filter(Investments.month == todayDate.month
                                       and Investments.year == todayDate.year
                                       and Investments.username == current_user.username).all()
    
    total_investments = sum_query_cost(investments)
    
    

    insurance = Insurance.query.filter(Insurance.month == todayDate.month 
                                   and Insurance.year == todayDate.year
                                   and Insurance.username == current_user.username).all()

    total_insurance = sum_query_cost(insurance)
    

    family_entertainment = Familyentertainment.query.filter(Familyentertainment.month == todayDate.month
                                                        and Familyentertainment.year == todayDate.year
                                                        and Familyentertainment.username == current_user.username).all()
    
    total_entertainment = sum_query_cost(family_entertainment)
    
    

    takeaways = Takeaway.query.filter(Takeaway.month == todayDate.month
                                  and Takeaway.year == todayDate.year
                                  and Takeaway.username == current_user.username).all()
    
    total_takeaway = sum_query_cost(takeaways)
    
    current_food = Workfood.query.filter(Workfood.month == todayDate.month
                                     and Workfood.year == todayDate.year
                                     and Workfood.username == current_user.username).all()

    workfood_total = sum_query_cost(current_food)
    

    #Uses helper function to extract float values from database query
    #Uses helper function on the object of floates to total debits/credits in the provided query object 
      
    combined_totals = [extra_groceries_total, workfood_total, total_takeaway, total_transport, total_subscriptions, total_investments, total_entertainment] 
    
    sum_multiline_items = sum_combined_totals(combined_totals)
    
      
    remaining = (credit_total_single_values + sum_multiline_items) - debit_total
    remaining_formatted = '{:.2f}'.format(remaining)
    

    return render_template('accounts.html', 
                           user=current_user,
                           current_month_text=current_month_text, 
                           account=account, 
                           active=active,
                           credits=credits,
                           rollover=rollover, 
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
    
    #reminder account is the form instance and therefore checks if an input was provided.
    #active is the query object from querying account
     
    zero = find_zero_balance(active)
    print(zero)

    if account.salary_deposit.data:
      credits.salary_deposit = account.salary_deposit.data

    if account.windfall.data:
      credits.windfall = account.windfall.data

    #Rent Section Start
    print("Rent section start")
    
    #If the form has a number > 0 in the submit
    if account.rent.data != None and account.rent.data > 0:
      # then save it to the active object and commit it back to the database
      active.rent = account.rent.data
      print("rent data")
      print(account.rent.data)
    # If the queried rent lock starts out False but the form rent_lock is True 
    if rollover.rent_lock == False and account.rent_lock.data == True:
      # Then save the True back to the rollover table
      rollover.rent_lock = account.rent_lock.data
      # If there is already a rent stored in the active table
      if active.rent > 0:
        # Then also save it to the fixed rent table
        rollover.rent_fixed = active.rent
      # else if there is a rent in the current form submi
      elif account.rent.data > 0:
        # Then also save that to the fixed rent table
        rollover.rent_fixed = active.rent
    # If the queried rent lock starts out True but the form rent_lock is False
    elif rollover.rent_lock == True and account.rent_lock.data == False:
      # Then save the False back to the rent_lock to the rollover table
      rollover.rent_lock = account.rent_lock.data
      # Clear the value saved in the rent_fixed table 
      rollover.rent_fixed = 0
      # Clear the value in the active table so that it enables the submission of a new value
      active.rent = 0
      
      #Rent section ends 
          
    # Houskeeping starts here     
    if account.housekeeping.data:
      active.housekeeping = account.housekeeping.data

    

    # Water section starts here
    print("Water section start")
    
    #If the form has a number > 0 in the submit
    if account.water.data != None and account.water.data > 0:
      # then save it to the active object and commit it back to the database
      active.water = account.water.data
      print("water data")
      print(account.water.data)
    # If the queried water lock starts out False but the form water_lock is True 
    if rollover.water_lock == False and account.water_lock.data == True:
      # Then save the True back to the rollover table
      print("water lock is")
      print(account.water_lock.data)
      rollover.water_lock = account.water_lock.data
      # If there is already a rent stored in the active table
      if active.water > 0:
        # Then also save it to the fixed rent table
        rollover.water_fixed = active.water
      # else if there is a rent in the current form submi
      elif account.water.data > 0:
        # Then also save that to the fixed rent table
        rollover.water_fixed = active.water
    # If the queried rent lock starts out True but the form rent_lock is False
    elif rollover.water_lock == True and account.water_lock.data == False:
      # Then save the False back to the rent_lock to the rollover table
      rollover.water_lock = account.water_lock.data
      # Clear the value saved in the rent_fixed table 
      rollover.water_fixed = 0
      # Clear the value in the active table so that it enables the submission of a new value
      active.water = 0
        #Water section ends here

      # Electric section starts here
    print("Electric section start")
    
    #If the form has a number > 0 in the submit
    if account.electric.data != None and account.electric.data > 0:
      # then save it to the active object and commit it back to the database
      active.electric = account.electric.data
      print("electric data")
      print(account.electric.data)
    # If the queried water lock starts out False but the form Electric_lock is True 
    if rollover.electric_lock == False and account.electric_lock.data == True:
      # Then save the True back to the rollover table
      print("electric lock is")
      print(account.electric_lock.data)
      rollover.electric_lock = account.electric_lock.data
      # If there is already a Electric stored in the active table
      if active.electric > 0:
        # Then also save it to the fixed Electric table
        rollover.electric_fixed = active.electric
      # else if there is a Electric in the current form submi
      elif account.electric.data > 0:
        # Then also save that to the fixed rent table
        rollover.electric_fixed = active.electric
    # If the queried rent lock starts out True but the form Electric_lock is False
    elif rollover.electric_lock == True and account.electric_lock.data == False:
      # Then save the False back to the Electric_lock to the rollover table
      rollover.electric_lock = account.electric_lock.data
      # Clear the value saved in the Electric_fixed table 
      rollover.electric_fixed = 0
      # Clear the value in the active table so that it enables the submission of a new value
      active.electric = 0
        #Electric section ends here

    # Internet section starts here
    print("Internet section start")
    
    #If the form has a number > 0 in the submit
    if account.internet.data != None and account.internet.data > 0:
      # then save it to the active object and commit it back to the database
      active.internet = account.internet.data
      print("internet data")
      print(account.internet.data)
    # If the queried water lock starts out False but the form internet_lock is True 
    if rollover.internet_lock == False and account.internet_lock.data == True:
      # Then save the True back to the rollover table
      print("Internet lock is")
      print(account.internet_lock.data)
      rollover.internet_lock = account.internet_lock.data
      # If there is already a internet stored in the active table
      if active.internet > 0:
        # Then also save it to the fixed internet table
        rollover.internet_fixed = active.internet
      # else if there is a rent in the current form submi
      elif account.internet.data > 0:
        # Then also save that to the fixed internet table
        rollover.internet_fixed = active.internet
    # If the queried internet lock starts out True but the form internet_lock is False
    elif rollover.internet_lock == True and account.internet_lock.data == False:
      # Then save the False back to the internet_lock to the rollover table
      rollover.internet_lock = account.internet_lock.data
      # Clear the value saved in the internet_fixed table 
      rollover.internet_fixed = 0
      # Clear the value in the active table so that it enables the submission of a new value
      active.internet = 0
        #Internet section ends here

    # counciltax section starts here
    print("counciltax section start")
    
    #If the form has a number > 0 in the submit
    if account.counciltax.data != None and account.counciltax.data > 0:
      # then save it to the active object and commit it back to the database
      active.counciltax = account.counciltax.data
      print("internet data")
      print(account.counciltax.data)
    # If the queried water lock starts out False but the form counciltax_lock is True 
    if rollover.counciltax_lock == False and account.counciltax_lock.data == True:
      # Then save the True back to the rollover table
      print("counciltax lock is")
      print(account.counciltax_lock.data)
      rollover.counciltax_lock = account.counciltax_lock.data
      # If there is already a counciltax stored in the active table
      if active.counciltax > 0:
        # Then also save it to the fixed counciltax table
        rollover.counciltax_fixed = active.counciltax
      # else if there is a counciltax in the current form submit
      elif account.counciltax.data > 0:
        # Then also save that to the fixed counciltax table
        rollover.counciltax_fixed = active.counciltax
    # If the queried counciltax lock starts out True but the form counciltax_lock is False
    elif rollover.counciltax_lock == True and account.counciltax_lock.data == False:
      # Then save the False back to the counciltax_lock to the rollover table
      rollover.counciltax_lock = account.counciltax_lock.data
      # Clear the value saved in the counciltax_fixed table 
      rollover.counciltax_fixed = 0
      # Clear the value in the active table so that it enables the submission of a new value
      active.counciltax = 0
        #counciltax section ends here

    if account.fitness.data:
      active.fitness = account.fitness.data

    if account.bakery.data:
      active.bakery = account.bakery.data
      
    if account.shopping.data:
      active.shopping = account.shopping.data
  
  db.session.commit()  
  return redirect(url_for('accounts'))

@app.route('/workfood', methods=['GET', 'POST'])
@login_required
def workfood():
  foodform = WorkfoodForm()
  todayDate = datetime.now()
  todayMonth = int(todayDate.month)
  todayYear = int(todayDate.year)  
  
  if request.method == 'GET':
    sum_breakfast = 0
    sum_lunch = 0
    sum_social = 0
    sum_snacks_me = 0
    sum_snacks_share = 0

    current_food = Workfood.query.filter(Workfood.month == todayMonth
                                         and Workfood.year == todayYear
                                         and Workfood.username == current_user.username).all()


    workfood_total = sum_query_cost(current_food)
    
    
    
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
                            workfood_total=workfood_total)

  if request.method == 'POST':
    sum_food = 0
    #Put an loop in here that checks for the data float and adds those together.
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


    new_workfood = Workfood(day=todayDate.day,
                            month=todayDate.month, 
                            year=todayDate.year, 
                            work_breakfast=foodform.work_breakfast.data, 
                            work_lunch=foodform.work_lunch.data, 
                            after_work_social=foodform.after_work_social.data, 
                            work_snacks_me=foodform.work_snacks_me.data, 
                            work_snacks_share=foodform.work_snacks_share.data,
                            username=current_user.username,
                            cost=sum_food)

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
    
    new_likesdislikes = Likesdislikes(likes_dislikes=form.likes_dislikes.data, 
                                      country=form.country.data, 
                                      reason=form.reason.data, 
                                      username=current_user.username)
    
    db.session.add(new_likesdislikes)
    db.session.commit()

    return redirect(url_for('index'))
    
@app.route('/subscriptions', methods=['GET', 'POST'])
def subscriptions():
  todayDate = datetime.now()
  todayMonth = int(todayDate.month)
  todayYear = int(todayDate.year)
  subs = SubscriptionsForm()
  if request.method == 'GET':

    current_subscriptions = Subscriptions.query.filter(Subscriptions.month == todayMonth
                                                   and Subscriptions.year == todayYear
                                                   and Subscriptions.username == current_user.username).all()

    return render_template('subscriptions.html', subs=subs, current_subscriptions=current_subscriptions)

  if request.method == 'POST':
    #if the term is monthly add a month to the start date and save it as the auto renewal
    if subs.subscription_term.data == 'Monthly':
      print("We need to add a month to the auto renewal date")
      days_in_month = calendar.monthrange(subs.subscription_start_date.data.year, subs.subscription_start_date.data.month)[1]   
      add_auto_renew = subs.subscription_start_date.data + timedelta(days=days_in_month)
    #else it must be yearly so add a year to the start date and save that as the auto renewal
    else:
      add_auto_renew=subs.subscription_start_date.data.replace(year=subs.subscription_start_date.data.year + 1)

    new_subscriptions = Subscriptions(month = todayDate.month,
                                      year = todayDate.year,
                                      subscription_name=subs.subscription_name.data,
                                      subscription_term=subs.subscription_term.data,
                                      subscription_start_date=subs.subscription_start_date.data,
                                      subscription_auto_renewal=add_auto_renew,
                                      cost=subs.cost.data,
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
                                  cost=inv.investment_cost.data,
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
                              cost=ins.insurance_cost.data,
                              username=current_user.username)

    db.session.add(new_insurance)
    db.session.commit()
    return redirect(url_for('insurance'))


@app.route('/extra_groceries', methods=['GET', 'POST'])
@login_required
def extragroceries():
  todayDate = datetime.now()
  todayMonth = int(todayDate.month)
  todayYear = int(todayDate.year)
  extra = ExtragroceriesForm()
  monthNow = month_from_number(todayDate.month)

  if request.method == 'GET':
    
    extra_groceries = Extragroceries.query.filter(Extragroceries.month == todayMonth
                                              and Extragroceries.year == todayYear
                                              and Extragroceries.username == current_user.username).all()

    list = []
    for l in extra_groceries:
      space = l.grocerydescription.split(' ')
      for s in space:
        list.append(s)
      for a in list:
        print(a)
  
    
    return render_template('extragroceries.html', extra=extra, list=list, monthNow=monthNow)

  if request.method == 'POST' and extra.validate():
    new_groceries = Extragroceries(day=todayDate.day,
                                   month=todayDate.month, 
                                   year=todayDate.year,
                                   grocerydescription=extra.extra_groceries_description.data,
                                   cost=extra.extra_groceries.data,
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
  todayMonth = int(todayDate.month)
  todayYear = int(todayDate.year)

  if request.method == 'GET':
    total_train = 0
    total_bus = 0
    total_uber = 0
    total_taxi = 0
    total_plane = 0
    method_totals = []

    get_transp = Transport.query.filter(Transport.month==todayMonth
                                        and Transport.year==todayYear
                                        and Transport.username == current_user.username).all()
    

    if get_transp != None:
      for method in get_transp:
        if method.method_of_travel == 'Train':
          total_train += method.cost
        elif method.method_of_travel == 'Bus':
          total_bus += method.cost
        elif method.method_of_travel == 'Uber':
          total_uber += method.cost
        elif method.method_of_travel == 'Taxi':
          total_taxi += method.cost
        elif method.method_of_travel == 'Plane':
          total_plane += method.cost

    method_totals.append(total_train)
    method_totals.append(total_bus) 
    method_totals.append(total_uber) 
    method_totals.append(total_taxi)
    method_totals.append(total_plane)
    

    transport_methods = ['Train', 'Bus', 'Uber', 'Taxi', 'Plane']
    
    
    return render_template('transport.html', transp=transp, current_month=current_month, transport_methods=transport_methods, method_totals=method_totals)

  if request.method == 'POST' and transp.validate():

    new_transport = Transport(month=todayDate.month, 
                              year=todayDate.year,
                              destination=transp.destination.data,
                              method_of_travel=transp.method_of_travel.data,
                              cost=transp.cost_of_travel.data,
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
  
  if request.method == 'POST' and FamilyentForm:
    new_entertainment = Familyentertainment(day=todayDate.day, 
                                            month=todayDate.month, 
                                            year=todayDate.year, 
                                            entertainment_title=FamilyentForm.entertainment_title.data,
                                            entertainmnet_description=FamilyentForm.entertainment_description.data,
                                            cost=FamilyentForm.entertainment_cost.data,
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
                            cost=takeaway.takeaway_cost.data)

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
    
    thoughts = Thinking.query.filter(Thinking.timestamp > new_date).all()
    return render_template('thoughtsreport.html', thoughts=thoughts)

@app.route('/lifehacks_report')
@login_required
def lifehacksreport():
  if request.method == 'GET':
    new_date = datetime.now() - timedelta(days = 30)
    hacks = Life_hacks.query.filter(Life_hacks.date > new_date).all()
    
    return render_template('lifehacks_report.html', hacks=hacks)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def testdelete(id):
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





    
  
