from mongoengine import Document
from mongoengine.fields import StringField,DateTimeField
from datetime import datetime
class Project(Document):
  name = StringField(required=True)
  description = StringField(required=True)
  created_by= StringField(required=True)
  created_at=DateTimeField(default=datetime.utcnow)




