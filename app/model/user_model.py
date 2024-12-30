from mongoengine import Document
from mongoengine.fields import StringField
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    role= StringField(default="user")

    def set_password(self, password: str):
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str):
        return pwd_context.verify(password, str(self.password))
