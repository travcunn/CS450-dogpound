from datetime import datetime

from flask import flash, g, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required, login_user, \
    logout_user

from app import app, db, login_manager, models
from app.forms import BarkForm, LoginChecker, LoginForm
from app.models import User, Bark


login_manager.login_view = 'login'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """Route for the home page."""
    # display the bark form and feed
    form = BarkForm()

    if form.validate_on_submit():
    # record bark in database and attach to active user
        bark = Bark(barkBody=form.barkBody.data, timestamp=datetime.utcnow(),
                    author=g.user)
        db.session.add(bark) 
        db.session.commit() # commit database add
        form.barkBody.data = '' # clear form field for bark

        # display all the barks in the database - 
        # <<< will need to filter to own posts and friends posts only >>>
        # order newest to oldest
    barks = models.Bark.query.order_by('timestamp desc').all()

    return render_template('index.html', title='Home', user=g.user,
                           barks=barks, form=form)
							

@app.route("/login", methods=['GET', 'POST'])
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

    return render_template('login.html', form=login_form)


@app.route("/logout")
def logout():
    """Redirect page for invalid logins."""  
    logout_user()
    flash('You have been logged out.')
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
