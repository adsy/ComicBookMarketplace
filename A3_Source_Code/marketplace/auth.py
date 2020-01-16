#import important modules
from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from .models import User
from .forms import LoginForm, RegisterForm
from . import db
from flask_login import login_user, login_required,logout_user

#for password storage
from werkzeug.security import generate_password_hash,check_password_hash

#allows user ID retrieval
from flask import session

#create a blueprint for authentication
bp = Blueprint('auth', __name__)

#Create a function to handle user login
@bp.route('/login', methods = ['GET', 'POST'])
def login():

  #Create new user login form
  form = LoginForm()

  #Set error to none
  error=None

  #If form is validated on submission
  if(form.validate_on_submit()):
    username = form.username.data
    password = form.password.data

    #Grab details of user
    u1 = User.query.filter_by(name=username).first()
    
    #if there is no user with that name
    if u1 is None:
      error='Incorrect user name'
    #check the password - notice password hash function
    elif not check_password_hash(u1.password_hash, password): # takes the hash and password
      error='Incorrect password'
    if error is None:
    #all good, set the login_user
      msg='Login succesful'
      login_user(u1)      
      print(msg)
      flash(msg)

      #allow user id retrievel
      session['id'] = u1.id

      #Redirect user to comic dashboard
      return redirect(url_for('comic.manage'))
    #Print error if there was a problem
    else:
      print(error)
      flash(error)
    #it comes here when it is a get method
  return render_template('user_form.html', form=form, heading='Login')

#Create function for user logging out
@bp.route('/logout')
@login_required
def logout():
    #removes id from session
    session.pop('id')
    logout_user()
    return redirect(url_for('main.index'))

#Create function to handle user registration
@bp.route('/register', methods = ['GET', 'POST'])  
def register():  

    #Create registration form for user
    form = RegisterForm()

    #If form validate on submit
    if form.validate_on_submit():

      print('Register form submitted')
       
      #get username, password and email from the form
      uname =form.username.data
      pwd = form.password.data
      email=form.email.data
      
      # don't store the password - create password hash
      pwd_hash = generate_password_hash(pwd)
      
      #create a new user model object
      new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
      
      #Add new user to DB
      db.session.add(new_user)
      
      #Save changes to DB
      db.session.commit()
      
      #commit to the database and redirect to HTML page
      return redirect(url_for('auth.login'))
    
    #Render page with variables
    return render_template('user_form.html', form=form, heading='Register')








  
    