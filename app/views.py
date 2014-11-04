from flask import render_template, flash, redirect
from app import app, db, models
from .forms import LoginForm, BarkForm
from .models import User, Bark
from datetime import datetime


# home page route
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
# display the bark form and feed
	form = BarkForm()
# 	user = {'firstName': 'Marty', 'lastName':'McFly', 'email':'marty@delorean.com'} #test user
# set user to user 1 until login feature is working
	user = models.User.query.get(1)
	if form.validate_on_submit():
# 	record bark in database and attach to active user
		bark = Bark(barkBody=form.barkBody.data, timestamp=datetime.utcnow(), author=user)
		db.session.add(bark) 
		db.session.commit() #commit database add
		form.barkBody.data='' #clear form field for bark

# display all the barks in the database - <<< will need to filter to own posts and friends posts only >>>
	barks = models.Bark.query.all()

# 	sample barks
	# barks = [
# 		{
# 			'author' : {'email': 'vader@deathstar.com','firstName': 'Darth', 'lastName': 'Vader'},
# 			'body': "That's no moon."
# 		},
# 		{
# 			'author' : {'email': 'luke@rebelbase.com', 'firstName': 'Luke', 'lastName': 'Skywalker'},
# 			'body': "No, that's not true...that's impossible!"	
# 		}
# 	]
	
	return render_template('index.html', 
							title='Home',
							user=user,
							barks=barks,
							form=form)
							

# login page							
@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
# 	temporarily set loggedIn to False until that code is written
	loggedIn=False
	if form.validate_on_submit():
# 	flash message to display to the user
		flash('Login requested for email="%s", password=%s, remember_me=%s' %
			(form.email.data, form.password.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template('login.html', 
							title='Sign In', 
							form=form,
							loggedIn=loggedIn)

# redirect page for invalid logins    
@app.route("/invalid")
def invalid():
	
	return render_template('invalid.html', title='Invalid Login Attempt', loggedIn=False)