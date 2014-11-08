from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    """
    Login form and it's fields.
    """
    # email and password are required fields
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class BarkForm(Form):
    """
    New bark form.
    """
    barkBody = StringField('bark', validators=[DataRequired()])


class RegistrationForm(Form):
    """
    Registration form and it's fields. All of the fields are required.
    """
    firstName = StringField('firstName', validators=[DataRequired()])
    lastName = StringField('firstName', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
