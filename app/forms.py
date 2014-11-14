from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired
from flask.ext.bcrypt import Bcrypt

from app import app, db
from app.models import User

bcrypt = Bcrypt(app)

class LoginForm(Form):
    """
    Login form and it's fields.
    """
    # email and password are required fields
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class LoginChecker(object):
    """
    Form that checks if a login is valid.
    """

    
    def __init__(self, email, password):
        self._email = email
        self._password = password

    @property
    def is_valid(self):
        user = self.lookup_user
        if user is not None:    
        	# check typed password against hashed pw in DB
			if bcrypt.check_password_hash(user.password, self._password):
				return True
			
        # if user.password != self._password:
#             return False

        return False

    @property
    def lookup_user(self):
        return db.session.query(User).filter_by(email=self._email).first()


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
    password = PasswordField('password', validators=[DataRequired()])
    password_match = PasswordField('password_match', validators=[DataRequired()])