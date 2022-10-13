from flask import Blueprint, render_template, request,flash,url_for,redirect
from flask_jwt import jwt_required

from App.database import db

from App.controllers import(
    create_user,
    create_form,
    authenticate,
    login_user
)

from App.models import User

signup_views = Blueprint('signup_views', __name__, template_folder='../templates')

@signup_views.route('/signUp', methods = ['POST'])
def signUp():
  userdata = request.get_json() 

  newuser = User(username = userdata['username'], email = userdata['email'], password = userdata['password'])
  newuser.set_password(userdata['password'])
  
  # try:
  db.session.add(newuser)
  db.session.commit() # save user
  # except IntegrityError: # attempted to insert a duplicate user
    # db.session.rollback()
    # return 'Username or Email already exists. Try Again.' # error message
  return 'New Teacher Account Created'

  
@signup_views.route('/login')
def login_page():
    userdata = request.get_json() 
    user = authenticate(userdata['username'], userdata['password'])
    if user:
      return 'Logged In'
    else:
      return 'Cannot be authenticated.'

