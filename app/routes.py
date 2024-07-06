import os
from flask import Blueprint, render_template, redirect, request, send_from_directory, flash
from random import choice, randint
import bcrypt

from flask_login import login_required, login_user, logout_user
from werkzeug.utils import secure_filename

from app import db
from app.models import User, Project, Media
from app.forms import LoginForm

routes = Blueprint( 'routes', __name__ )

@routes.route( '/', methods=[ 'GET', 'POST' ] )
def index():
  images = list()

  for _ in range( 20 ):
    w = 100 * randint(2, 4)
    h = 100 * randint(2, 4)
    images.append( f"https://picsum.photos/{w}/{h}" )
  #
  return render_template( 'index.html', images=images )
#

# @routes.route( '/favicon.ico' )
# def favicon():
#   return send_from_directory( os.path.join( app.root_path, 'static' ), 'ntern.png' )

@routes.route( '/login', methods=[ 'GET', 'POST' ] )
def login():
  form = LoginForm()

  # /login is hit again when the form is submitted
  if form.validate_on_submit():
    u = User.query.filter_by( name=form.name.data ).first()

    # encode form data as bytes and compare to the hash stored in the database
    if u and bcrypt.checkpw( str.encode( form.password.data ), str.encode( u.password ) ):
      login_user( u )
      return redirect( request.args.get( 'next' ) or 'admin' )
    #
    else:
      flash( f"THAT WASN'T VERY CORRECT", "danger" )
    #
  #
  return render_template( 'login.html', form=form )
#

@routes.route( '/logout' )
@login_required
def logout():
  logout_user()
  return redirect( '/' )
#
