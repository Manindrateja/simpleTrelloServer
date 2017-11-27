from base import Base,db
from users import User

class Task(Base):
	name = db.StringField(required = True)
	# title = db.StringField(required = True)
	createdBy = db.ReferenceField(User)
	assignedTo = db.ReferenceField(User)
	description = db.StringField()
	orderNumber = db.IntField()

	def transform(self):
		return{
			'id' : self.get_id(),
			'name': self.name, 
			# 'title': self.title,
			# 'createdBy': self.createdBy.transform(),
			# 'assignedTo': self.assignedTo.transform(), 
			# 'description': self.description,
			'orderNumber': self.orderNumber
		}

class List(Base):
	name = db.StringField(required = True)
	tasklists = db.ListField(db.ReferenceField(Task))
	orderNumber = db.IntField()

	def transform(self):
		return{
			'id': self.get_id(),
			'tasklists': self.tasklists,
			'orderNumber': self.orderNumber,
			'name': self.name
		}

	def getAll(self):
		return{
			'id': self.get_id(),
			'tasklists': [task.transform() for task in self.tasklists],
			'orderNumber': self.orderNumber,
			'name': self.name
		}

class Board(Base):
	name = db.StringField(required = True)
	owner = db.ReferenceField(User)
	isShared = db.BooleanField(default = False)
	members = db.ListField(db.ReferenceField(User))
	lists = db.ListField(db.ReferenceField(List))

	def transform(self):
		return {
			'name': self.name,
			'owner': self.owner.transform(),
			'isShared': self.isShared,
			'members': self.members,
			'lists': self.lists,
			'id': self.get_id()
		}

	def get_meta(self):
		return{
			'name': self.name,
			'id': self.get_id(),
			'owner': self.owner.transform()
		}

	def getAll(self):
		return{
			'name': self.name,
			'owner': self.owner.transform(),
			'isShared': self.isShared,
			'members': [member.transform() for member in self.members],
			'lists': [item.getAll() for item in self.lists],
			'id': self.get_id()
		}	