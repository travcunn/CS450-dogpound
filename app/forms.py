from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

# class for the login form and fields
class LoginForm(Form):

# email and password are required fields
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

# class for the new barks form
class BarkForm(Form):
	barkBody = StringField('bark', validators=[DataRequired()])