from app import db

friends = db.Table('friends',
    db.Column('friender_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('friendee_id', db.Integer, db.ForeignKey('user.id')))  

# user class for database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    firstName = db.Column(db.String(80), index=True)
    lastName = db.Column(db.String(80), index = True)
    password = db.Column(db.String(20), index=True)
	#  adds relationship between User and Barks so a user's barks can be displayed
    barks = db.relationship('Bark', backref='author', lazy='dynamic')
    friendList = db.relationship('User', 
    							secondary=friends,
    							primaryjoin=(friends.c.friender_id == id),
    							secondaryjoin=(friends.c.friendee_id == id),
    							backref=db.backref('friends', lazy='dynamic'),
    							lazy='dynamic')
    
    def friends_barks(self):
    	return Bark.query.join(friends, 
    		(friends.c.friendee_id == Bark.user_id)).filter(friends.c.friender_id == self.id).order_by(Bark.timestamp.desc())
    
	#  return the user's first name
    def __repr__(self):
        return '<User %r>' % (self.firstName)
      
        
#  Bark class for collection of barks in the feed 
class Bark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barkBody = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
	#  adds foreign key to tie each bark to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	#  return the bark body
    def __repr__(self):
        return '<Bark %r>' % (self.barkBody)