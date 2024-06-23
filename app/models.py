from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

from typing import Set
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship


class Base( DeclarativeBase ):
  pass


class Project( Base ):
  __tablename__ = 'project'

  project_id  : Mapped[int] = mapped_column( primary_key=True )
  title       : Mapped[str] = mapped_column( String(50), nullable=False )
  description : Mapped[str] = mapped_column( String )
  directory   : Mapped[str] = mapped_column( String )
  media       : Mapped[Set["Media"]] = relationship()


class Media( Base ):
  __tablename__ = 'media'

  media_id   : Mapped[int] = mapped_column( primary_key=True )
  project_id : Mapped[int] = mapped_column( ForeignKey( "project.project_id" ) )
  filename   : Mapped[str] = mapped_column( String )
  preview    : Mapped[bool] = mapped_column( Boolean )


class User( UserMixin, db.Model ):
  __tablename__  = 'user'

  uid           = db.Column( db.Integer, autoincrement=True, primary_key=True )
  name          = db.Column( db.String( 30 ) )
  password      = db.Column( db.String( 100 ) ) # encrypted
  authenticated = db.Column( db.Boolean, default=False )

  def get_id( self ):
    return self.uid

  def __repr__( self ):
    return f'[User, id={ self.uid }, name="{ self.name }"]'


@login_manager.user_loader
def load_user( uid ):
  return User.query.get( int( uid ) )
