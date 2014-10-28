dogpound
========
A twitter-like service for animals other than birds.


Requirements
============
You will need the following to setup dogpound:
- Python 2.7
- pip
- virtualenv


Installation
============
```
git clone https://github.iu.edu/CS450-ECE461/fall2014-group8.git
cd fall2014-group8.git
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Development
===========
Before developing, it is important to setup a virtualenv (a virtual environment). To do so, create a new virtualenv (unless it already exists, skip this step):
```
virtualenv venv
```
Then activate it:
```
source venv/bin/activate
```


Running tests
=============
```
make test
```

Running the web app
===================
```
make run
```
