
from flask_sqlalchemy import SQLAlchemy
from flask import Flask 
from os import path 
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY']="mjay"
  app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
  
  db.init_app(app)
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)
  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))
  
  from .auth import auth
  from .views import views
  
  app.register_blueprint(auth, url_prefix='/') 
  app.register_blueprint(views,url_prefix='/')
  from .models import User
  with app.app_context():
        db.create_all()

  
  return app