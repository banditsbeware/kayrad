import shutil
import os
from flask_login import UserMixin
from app import db, login_manager

from typing import Set
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

class Project( db.Model ):
  __tablename__ = 'project'

  p_id        : Mapped[int] = mapped_column( primary_key=True )
  title       : Mapped[str] = mapped_column( String(50), nullable=False )
  description : Mapped[str] = mapped_column( String )
  directory   : Mapped[str] = mapped_column( String )
  media       : Mapped[Set["Media"]] = relationship()

  def save( self ):
    db.session.add( self )
    db.session.commit()
  #

  def delete( self ):
    for m in self.media: m.delete()

    # well.. it really should exist...
    if os.path.exists( self.directory ):
      shutil.rmtree( self.directory )
    #

    db.session.delete( self )
    db.session.commit()
  #
#

class Media( db.Model ):
  __tablename__ = 'media'

  media_id   : Mapped[int] = mapped_column( primary_key=True )
  p_id       : Mapped[int] = mapped_column( ForeignKey( "project.p_id" ) )
  filename   : Mapped[str] = mapped_column( String )
  preview    : Mapped[bool] = mapped_column( Boolean )

  def save( self, file_data ):
    project = Project.query.get( self.p_id )

    file_data.save( os.path.join( project.directory, file_data.filename ) )
    db.session.add( self )
    db.session.commit()
  #

  def delete( self ):
    project = Project.query.get( self.p_id )

    m_path = os.path.join( project.directory, self.filename )
    if os.path.exists( m_path ):
      os.remove( m_path )
    #
    db.session.delete( self )
    db.session.commit()
  #
#

class User( UserMixin, db.Model ):
  __tablename__  = 'user'

  uid           = db.Column( db.Integer, autoincrement=True, primary_key=True )
  name          = db.Column( db.String( 30 ) )
  password      = db.Column( db.String( 100 ) ) # encrypted
  authenticated = db.Column( db.Boolean, default=False )

  def get_id( self ):
    return self.uid
  #

  def __repr__( self ):
    return f'[User, id={ self.uid }, name="{ self.name }"]'
  #
#

@login_manager.user_loader
def load_user( uid ):
  return User.query.get( int( uid ) )
#