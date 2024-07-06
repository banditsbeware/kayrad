import shutil
import os
from flask import Blueprint, render_template, redirect, request
from flask_login import current_user, login_required 

import app
from app.models import User, Project, Media

project = Blueprint( 'project', __name__ )

@project.route( '/' )
# @login_required
def root():
  return render_template( 'admin.html', 
    projects=Project.query.all()
  )
#

@project.route( '/edit/<int:p_id>' )
# @login_required
def edit( p_id ):
  if p_id == 0:
    return redirect( '/project' )
  #
  p_editing = Project.query.get( p_id )

  media = list()
  for m in Media.query.filter_by( p_id=p_id ).all():
    media.append( os.path.join( p_editing.directory, m.filename ) )
  #

  return render_template( 'admin.html', 
    editing=p_editing, 
    projects=Project.query.all(),
    media=media
  )
#

@project.route( '/save', methods=['POST'] )
# @login_required
def save():
  project = None
  p_id         = request.form.get( 'p_id' )
  _title       = request.form.get( 'title' )
  _description = request.form.get( 'description' )
  _directory   = f"instance/uploads/{ _title }"

  # match a preexisting title
  if (_project := Project.query.filter_by( title=_title ).first()):
    p_id = _project.p_id
  #

  if p_id:
    # edit an existing project
    project = Project.query.get( p_id )

    # if the title changed, move files to the new directory
    orig_directory = project.directory
    if _directory != orig_directory:
      print( f"'{_directory}' != '{orig_directory}'")
      shutil.move( orig_directory, _directory )      
    #
  #
  else:
    # create a new project
    project = Project()
    print( f"creating new project")
    os.makedirs( _directory )
  #

  project.title       = _title
  project.description = _description 
  project.directory   = _directory
  project.save()

  print( f"project {project.p_id}")

  files = request.files.getlist("files")
  for f in files:
    if f.filename:
      media = Media()
      media.p_id = project.p_id
      media.filename = f.filename
      media.preview = True # request.form.get( 'preview' ) is not None
      f.save( os.path.join( _directory, f.filename ) )
      media.save()
    #
  #
  return redirect( '/project' )
#

@project.route( '/delete', methods=['POST'] )
# @login_required
def delete():
  p_id = request.form.get( 'p_id' )
  if p_id: 
    project = Project.query.get( p_id ) 

    # well.. it really should exist...
    if os.path.exists( project.directory ):
      shutil.rmtree( project.directory )

    project.delete()
  return edit( 0 )
#

# @project.route( '/post/<int:i>' )
# def post( i ):
#   p = Project.query.get( i )
#   return render_template( 'post.html', 
#     back=True, 
#     title=p.title, 
#     body=p.body 
#   )
