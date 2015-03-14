from mongoengine import *
from mongoengine.django.auth import User
from datetime import datetime

# class Filee(Document):
#     file_name = StringField(max_length=100,required=True)

class Repof(Document):
    repo_url = StringField(max_length=100,required=True)
    last_update = DateTimeField(default=datetime.today())
    files = ListField()



class AutonUser(User):
    repos = ListField(ReferenceField(Repof))


class Webhook(Document):
    msg = StringField(default="")

