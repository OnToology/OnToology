from mongoengine import *
#from mongoengine.django.auth import User
from datetime import datetime
from mongoengine.django.auth import User



class Repo(Document):
    url = StringField(max_length=100,default='Not set yet')
    last_used = DateTimeField(default=datetime.now())
    created_on = DateTimeField(default=datetime.now())
    monitoring = StringField(max_length=100,default='Not set yet')
    state = StringField(max_length=50,default='Ready')
    owner = StringField(max_length=50,default='no')





class OUser(User):
    repos = ListField(ReferenceField(Repo))



