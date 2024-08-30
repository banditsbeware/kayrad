import os
from flask import Flask, Blueprint, render_template, request, make_response
from flask_login import LoginManager
from flask_cors import CORS

import configparser

config = configparser.ConfigParser()
config.read( os.path.abspath( "config.ini" ) )

login_manager = LoginManager()

def create_app():
    app = Flask( __name__ )
    app.config[ 'SECRET_KEY' ] = os.urandom( 32 )
    app.config[ 'MONGO_URI' ] = config['TEST']['DB_URI']

    from .routes import routes
    app.register_blueprint( routes, url_prefix='/' )

    from .project import project
    app.register_blueprint( project, url_prefix='/project' )

    login_manager.init_app( app )
    login_manager.login_view = 'routes.login'

    CORS( app )

    return app
