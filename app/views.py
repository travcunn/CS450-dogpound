from datetime import datetime

from flask import flash, g, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required, login_user, \
    logout_user
from flask.ext.bcrypt import Bcrypt

from app import app, db, login_manager
from app.forms import BarkForm, LoginChecker, LoginForm, EmailForm, RegistrationForm, ForgotPWChecker, ResetPWChecker, ResetPasswordForm, FollowForm
from app.models import Bark, Friendship, User

login_manager.login_view = 'login'

global tempUser
tempUser =''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """Route for the home page."""
    # display the bark form and feed
    form = BarkForm()
    
    #form for following other users by email address
    follow_form = FollowForm()

    if form.validate_on_submit():
    # record bark in database and attach to active user
        bark = Bark(barkBody=form.barkBody.data, timestamp=datetime.utcnow(),
                    author=g.user)
        db.session.add(bark) 
        db.session.commit() # commit database add
        form.barkBody.data = '' # Clear form field once bark is committed


    # display all the barks in the database - 
    # <<< filter to own posts and friends posts only >>>
    # order newest to oldest

    all_barks = Bark.query.order_by(Bark.timestamp.desc()).all()
    friendships = Friendship.query.filter(Friendship.user_id==g.user.id).all()
    friend_ids = [x.friend_id for x in friendships]
    valid_bark = [lambda x: x.author.id in friend_ids,
                  lambda x: x.author==g.user]
    def is_valid_bark(bark):
        for rule in valid_bark:
            if rule(bark):
                return True
        return False

    friends_barks = [bark for bark in all_barks if is_valid_bark(bark)]

    return render_template('index.html', title='Home', user=g.user,
                           barks=friends_barks, form=form, followForm=follow_form, loggedIn=is_logged_in())
							

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route for the login page."""

    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    login_form = LoginForm(request.form)

    if login_form.validate_on_submit():
        login = LoginChecker(email=request.form.get('email'),
                             password=request.form.get('password'))
        if login.is_valid:
            login_user(login.lookup_user, remember=True)
            return redirect(url_for('index'))
        flash('Invalid Login', 'danger')

    return render_template('login.html', title='Log In', form=login_form)
    
    
@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    """Route for the forgot password page."""

#     if g.user is not None and g.user.is_authenticated():
#         return redirect(url_for('index'))

    login_form = EmailForm(request.form)
    all_users = User.query.all()
    set_user(request.form.get('email'))
    
    if login_form.validate_on_submit():
    	for user in all_users:
    		if (request.form.get('email') == user.email):
    			return redirect(url_for('resetPassword'))		
    	flash('Invalid User Email', 'danger')
    	
    return render_template('forgotPassword.html', title='Forgot Password', form=login_form)

    
@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    """Route for the reset password page."""
    bcrypt = Bcrypt(app)
    # if g.user is not None and g.user.is_authenticated():
#         return redirect(url_for('index'))
	
    questions_form = ResetPasswordForm(request.form)
    user = User.query.filter_by(email=get_user()).first()
	
    if questions_form.validate_on_submit():
    	resetPW = ResetPWChecker(email=user.email, securityAnswer1=questions_form.securityAnswer1.data,
    		securityAnswer2=questions_form.securityAnswer2.data,
    		securityAnswer3=questions_form.securityAnswer3.data)
    	if resetPW.is_valid:
    		pw_hash = bcrypt.generate_password_hash(questions_form.password.data)
    		user.password = pw_hash
    		db.session.commit()
    		flash('Password reset! Please log in.', 'danger')
    		return redirect(url_for('login'))
    	flash('Answers to security questions incorrect. Please try again.', 'danger')
    	return redirect(url_for('forgotPassword'))
    	
    	
    return render_template('resetPassword.html', title='Reset Password', form=questions_form,
    						user=user)


@app.route("/registration", methods=['GET', 'POST'])
def register():
    """Route for the registration page."""
    bcrypt = Bcrypt(app)
	
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    registration_form = RegistrationForm(request.form)

    if registration_form.validate_on_submit():
    	pw_hash = bcrypt.generate_password_hash(registration_form.password.data) #generate hash for password
    	user = User(firstName=registration_form.firstName.data, 
    		lastName=registration_form.lastName.data, 
    		email=registration_form.email.data, 
    		password=pw_hash,
    		securityQuestion1=registration_form.securityQuestion1.data,
    		securityAnswer1=registration_form.securityAnswer1.data,
    		securityQuestion2=registration_form.securityQuestion2.data,
    		securityAnswer2=registration_form.securityAnswer2.data,
    		securityQuestion3=registration_form.securityQuestion3.data,
    		securityAnswer3=registration_form.securityAnswer3.data)
    	db.session.add(user)
    	db.session.commit() #commit database add
    	login = LoginChecker(email=request.form.get('email'), password=pw_hash)
    	flash('Successful Registration! Please log in.', 'danger')
    	return redirect(url_for('login'))
    	
	
	# if login.is_valid:
# 		login_user(login.lookup_user, remember=True)
# 		return redirect(url_for('index'))
# 	flash('Invalid Registration', 'danger')

    return render_template('registration.html', title='Register', form=registration_form)


@app.route("/logout")
def logout():
    """Redirect page for invalid logins."""  
    logout_user()
#     flash('You have been logged out.')
    return redirect(url_for('login'))


def is_logged_in():
    """Returns True if the user is logged in."""
    if g.user is not None and g.user.is_authenticated():
        return True
    return False


@app.before_request
def before_request():
    """Before the request, notify flask of the current user."""
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    """Returns a user, given a user id."""
    return User.query.get(int(id))
    
def set_user(userEmail):
    """Returns a user, given a user email."""
    global tempUser1
    tempUser1 = userEmail

def get_user():
    """Returns a user, given a user email."""
    return tempUser1
