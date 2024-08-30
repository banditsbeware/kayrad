import bson
from bson.objectid import ObjectId

import bcrypt

from werkzeug.local import LocalProxy

from flask import current_app, g
from flask_pymongo import PyMongo
from flask_login import UserMixin

from app import login_manager

class User( UserMixin ):
    def __init__( self, user_json ):
        self.user_json = user_json
    #

    def get_id( self ):
        object_id = self.user_json.get( '_id' )
        return str( object_id )
    #
#

@login_manager.user_loader
def load_user( user_id ):
    user_json = db.users.find_one( { "_id": ObjectId( user_id ) } )
    return User( user_json )
#

def get_db():
    db = getattr( g, "_database", None )

    if db is None: db = g._database = PyMongo( current_app ).db

    return db
#

db = LocalProxy( get_db )

def attr_if_exists( obj, attr ):
    return obj[attr] if attr in obj else None
#

def insert_or_update( project ):
    if "title" in project:
        db.projects.update_one(
            { # filter by title
                "title": project["title"]
            },
            { # update all fields
                "$set": {
                    "ptype"      : attr_if_exists( project, "ptype" ),
                    "description": attr_if_exists( project, "description" ),
                    "details":     attr_if_exists( project, "details" ),
                    "video":       attr_if_exists( project, "video" ),
                    "stills":      attr_if_exists( project, "stills" )
                }
            },
            # modify if this title exists; otherwise insert
            upsert=True
        )
        # return the ID of the upserted document
        return db.projects.find_one( { "title": project["title"] } )["_id"]
    #
    else:
        return None
    #
#

def add_user( name, password ):
    if db.users.find_one( { "name": name } ) is None:
        password_hash = bcrypt.hashpw( password.encode( 'utf-8' ), bcrypt.gensalt() )  
        db.users.insert_one( 
            {
                "name": name,
                "password": password_hash
            }
        )
    #
    else:
        print( f"user {name} already exists." )
    #
#

def check_password( user_name, password ):
    user_json = db.users.find_one( { "name": user_name } )
    if user_json is None:
        print( f"user {user_name} does not exist." )
    #
    else:
        if bcrypt.checkpw( password, user_json['password'] ):
            print( "correct!" )
        #
        else:
            print( "incorrect!" )
        #
    #
#
