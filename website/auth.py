from flask import Blueprint, render_template, request, url_for, flash, redirect 
from . import db
from flask_login import login_user, login_required, current_user, logout_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('pass')
    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        login_user(user, remember=True)
        return redirect(url_for('views.home'))
  return render_template('login.html')   
  
@auth.route('/register', methods=['GET', 'POST'])

def register():
  if request.method == 'POST':
    email = request.form.get('email')
    name = request.form.get('name')
    pass1 = request.form.get('pass1')
    pass2 = request.form.get('pass2')
    
    if pass1 == pass2:
      newUser = User(email=email, name=name, password=generate_password_hash(pass1, method = 'sha256')) 
      db.session.add(newUser)#.commit()
      db.session.commit()
      login_user(newUser, remember=True)
      flash('Signed up successfully!', category= 'success')
      return redirect(url_for('views.home'))
      
    else:
      print('error passed nor marxh')
      flash('password did not match!', category='error')
  return render_template('register.html')   


