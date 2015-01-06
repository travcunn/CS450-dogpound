Dogpound
========
A twitter-like service for animals other than birds.

Screenshots
===========
####Login
[![Login](https://github.iu.edu/CS450-ECE461/fall2014-group8/raw/master/misc/login.png)](https://github.iu.edu/CS450-ECE461/fall2014-group8/raw/master/misc/login.png)

####DogFeed
[![Home](https://github.iu.edu/CS450-ECE461/fall2014-group8/raw/master/misc/home.png)](https://github.iu.edu/CS450-ECE461/fall2014-group8/raw/master/misc/home.png)


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
Users are following other users from the same movie.

- vader@deathstar.com - noarms (Darth Vader)
- luke@rebelbase.com - TwinSister (Luke Skywalker)
- test@google.com - google1
- doc@delorean.com - Clara (Emmett Brown)
- marty@delorean.com - Jennifer (Marty McFly)
- harry@gasman.com - Samsonite (Harry Dunne)
- lloyd@aspen.com - PillsAreGood (Lloyd Christmas)
- han@falcon.com - Carbonite (Han Solo)
- ben@mail.com - OldMan (Obi-wan Kenobi)
- junior@gmail.com - Snakes (Indiana Jones)

Answers to security questions are the same for all users except junior
Food - Burgers
Pet - Spot
Year Born - 1980

Test Database is backed up as CSV files userDB, friendsDB, barksDB
