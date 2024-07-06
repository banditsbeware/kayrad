from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField
from wtforms.fields import StringField
from wtforms.fields import MultipleFileField
from wtforms.fields import PasswordField
from wtforms.fields import SubmitField
from wtforms.fields import SelectField
from wtforms.validators import InputRequired, Regexp

filename_regexp = r'^[^/\\]\.(jpg|png|mov)$'

class LoginForm( FlaskForm ):
  name      = StringField( 'Name', validators=[ InputRequired() ] )
  password  = PasswordField( 'Password', validators=[ InputRequired() ] )
  submit    = SubmitField( 'Log in' )