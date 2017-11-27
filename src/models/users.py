from base import Base,db
from datetime import datetime, timedelta

class User(Base):
	name = db.StringField(required=True)
	lname = db.StringField()
	email = db.StringField(required=True, unique=True)
	username = db.StringField(required=True, unique=True)
	password = db.StringField(required=True)

	def transform(self):
		return {
			'name' : self.name,
			'username' : self.username,
			'id': self.get_id(),
			'email': self.email
		}

class UserDetails(Base):
	user = db.ReferenceField(User)
	address = db.StringField()
	mobile = db.StringField()

class UserToken(Base):
	token = db.StringField(required = True)
	expiresAt = db.DateTimeField(required = True, default= datetime.now() + timedelta(days=7))
	user = db.ReferenceField(User)