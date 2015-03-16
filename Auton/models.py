from mongoengine import *
from mongoengine.django.auth import User
from datetime import datetime


# class Repof(Document):
#     repo_url = StringField(max_length=100,required=True)
#     state_code = StringField(max_length=100,default='not used yet')
#     token = StringField(max_length=100,default='not used yet')
#     files = ListField()



# class AutonUser(User):
#     repos = ListField(ReferenceField(Repof))


# class Webhook(Document):
#     msg = StringField(default="")

