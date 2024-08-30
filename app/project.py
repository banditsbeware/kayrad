from bson.objectid import ObjectId

import shutil
import os
from flask import Blueprint, current_app, render_template, redirect, request, url_for
from flask_login import current_user, login_required 

from app.db import *

project = Blueprint( 'project', __name__ )

def project_directory( dir ):
    return os.path.join( current_app.root_path, f"static/projects/{ dir }" )
#

# base case for administering the database
@project.route( '/' )
@login_required
def root():
    return render_template( 'admin-project.html', projects=db.projects.find() )
#

@project.post( '/save' )
@login_required
def save():
    project      = None
    p_id         = request.form.get( 'p_id' )
    title        = request.form.get( 'title' )
    ptype        = request.form.get( 'ptype' )
    description  = request.form.get( 'description' )
    details      = request.form.get( 'details' )
    video        = None
    stills       = list()

    # match a preexisting title
    if (_project := db.projects.find_one( { "title": title } )):
        p_id = _project["_id"]
    #

    # p_id came from the form (editing a project), or by looking up the title.
    # this ensures that "Create New" won't make a duplicate project if you re-use a title.
    # it assumes that you actually want to edit that project.
    if p_id:
        # edit an existing project
        project = db.projects.find_one( { "_id": ObjectId( p_id ) } )

        # if the title changed, move files to the new directory
        orig_title = project["title"]
        if title != orig_title:
            shutil.move( project_directory( orig_title ), project_directory( title ) )      
        #
        if "video"  in project: video  = project["video"]
        if "stills" in project: stills = project["stills"]
    #
    else:
        # create directory for the new project - video & stills are still empty here
        try:
            os.makedirs( project_directory( title ) )
        #
        except FileExistsError: pass
    #
    # save the stills
    fd_stills = request.files.getlist( "stills" )
    for file_data in fd_stills:
        if file_data.filename and file_data.filename not in stills:
            file_data.save( os.path.join( project_directory( title ), file_data.filename ) )
            stills.append( file_data.filename )
        #
    #
    # save the video
    fd_video  = request.files.get( "video" )
    if fd_video.filename and fd_video.filename.endswith( ".mp4" ):
        fd_video.save( os.path.join( project_directory( title ), fd_video.filename ) )
        video = fd_video.filename
    #
    # finished constructing the new/modified project
    project = {
        "title"      : title,
        "ptype"      : ptype,
        "description": description,
        "details"    : details,
        "video"      : video,
        "stills"     : stills
    }
    # write document to database
    p_id = insert_or_update( project )

    return edit_project( p_id )
#

@project.route( '/edit/<p_id>' )
@login_required
def edit_project( p_id ):
    try: 
        project = db.projects.find_one( { "_id": ObjectId( p_id ) } )
    #
    except:
        return root()
    #
    return render_template( 'admin-project.html', editing=project, projects=db.projects.find() )
#

@project.get( '/<p_id>' )
def view_project( p_id ):
    try: 
        project = db.projects.find_one( { "_id": ObjectId( p_id ) } )
    #
    except:
        return root()
    #
    return render_template( 'project.html', project=project )
#

@project.post( '/delete' )
@login_required
def delete_project():
    try: 
        project = db.projects.find_one( { "title": request.form.get( "title" ) } )
        if project is None: return root()
    #
    except:
        return root()
    #
    # delete directory and all files
    shutil.rmtree( project_directory( project["title"] ) )

    # remove project document from database
    db.projects.delete_one( { "_id": ObjectId( project["_id"] ) } )    

    return root()
#

@project.route( '/delete-file/<p_id>/<filename>' )
@login_required
def delete_file( p_id, filename ):
    try: 
        project = db.projects.find_one( { "_id": ObjectId( p_id ) } )
    #
    except:
        return root()
    #
    if filename is None or len( filename ) < 1: return root()

    # find and delete the file
    path = os.path.join( project_directory( project["title"] ), filename )
    if os.path.exists( path ): os.remove( path )

    # remove file from project object
    try:
        project["stills"].remove( filename )
    #
    except ValueError:
        if filename.endswith( ".mp4" ): project["video"] = None
    #

    # update document in database
    p_id = insert_or_update( project )

    return edit_project( p_id )
#
