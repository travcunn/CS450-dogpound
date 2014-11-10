[![Build Status](http://crunkcastle.noip.me:8080/buildStatus/icon?job=dogpound)](http://crunkcastle.noip.me:8080/job/dogpound/)
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



Test Users
==========
- vader@deathstar.com - noarms
- luke@rebelbase.com - TwinSister
- test@google.com - google1
