import shutil
import os
from flask import Blueprint, current_app, render_template, redirect, request, url_for
from flask_login import current_user, login_required 

from app.models import User, Project, Media

project = Blueprint( 'project', __name__ )

def project_directory( dir ):
    return os.path.join( current_app.root_path, f"static/projects/{ dir }" )

@project.route( '/' )
@login_required
def root():
  return render_template( 'admin.html', 
    projects=Project.query.all()
  )
#

@project.route( '/edit/<int:p_id>' )
@login_required
def edit( p_id ):
  if p_id == 0:
    return redirect( '/project' )
  #
  return render_template( 'admin.html', 
    editing=Project.query.get( p_id ), 
    projects=Project.query.all()
  )
#

@project.route( '/save', methods=['POST'] )
@login_required
def save():
  project = None
  p_id         = request.form.get( 'p_id' )
  _title       = request.form.get( 'title' )
  _description = request.form.get( 'description' )
  _directory   = project_directory( _title )

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
      shutil.move( orig_directory, _directory)      
    #
  #
  else:
    # create a new project
    project = Project()
    os.makedirs( _directory )
  #

  project.title       = _title
  project.description = _description 
  project.directory   = _directory
  if not project.media: project.media = set()
  project.save()

  files = request.files.getlist( "files" )
  for file_data in files:
    if file_data.filename:
      media = Media()
      media.p_id = project.p_id
      media.filename = file_data.filename
      media.preview = True # request.form.get( 'preview' ) is not None
      media.save( file_data=file_data )
      project.media.add( media )
    #
  #
  return redirect( url_for( "project.edit", p_id=project.p_id ) )
#

@project.route( '/delete', methods=['POST'] )
@login_required
def delete():
  p_id = request.form.get( 'p_id' )
  if p_id: 
    project = Project.query.get( p_id ) 
    project.delete()
  #
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
