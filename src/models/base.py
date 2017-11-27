from flask_mongoengine import MongoEngine
from datetime import datetime

# from abc import ABCMeta

db= MongoEngine()

class Base(db.Document):
    createdAt = db.DateTimeField()
    updatedAt = db.DateTimeField(default = datetime.now)
    meta = {
        "abstract": True
    }

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if not self.createdAt:
            self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        return super(Base, self).save(*args, **kwargs)

    def get_id(self):
        return self.id.__str__()
