from flask import Flask, render_template
app = Flask(__name__)

#from flask_wtf import Form
#from wtforms.ext.appengine.db import model_form
#from wtforms import validators
#from models import MyModel

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


# MyForm = model_form(MyModel, Form, field_args = {
#     'name' : {
#         'validators' : [validators.Length(max=10)]
#     }
# })

@app.route("/")
def hello():
    return "Dogpound homepage."
    
@app.route("/login")
def login():
    return render_template('login.html') + MyForm
    
@app.route("/feed")
def feed():
    return "Here is the dogfeed."

if __name__ == "__main__":
	app.run(debug=True)