import os
from flask import Flask, Blueprint, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'routes.login'

def create_app():
  app = Flask( __name__ )
  app.config[ 'UPLOAD_DIR' ] = 'uploads'
  app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///database.sqlite3'
  app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False
  app.config[ 'SECRET_KEY' ] = os.urandom( 32 )

  db.init_app( app )
  login_manager.init_app( app )

  from .routes import routes
  app.register_blueprint( routes, url_prefix='/' )

# from .blog import blog
# app.register_blueprint( blog, url_prefix='/' )

  return app
