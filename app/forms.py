from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class LoginForm( FlaskForm ):
  name      = StringField( 'Name', validators=[ InputRequired() ] )
  password  = PasswordField( 'Password', validators=[ InputRequired() ] )
  submit    = SubmitField( 'Log in' )
