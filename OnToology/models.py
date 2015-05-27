from mongoengine import Document,StringField,DateTimeField,ListField,ReferenceField
#from mongoengine.django.auth import User
from datetime import datetime





class Repo(Document):
    url = StringField(max_length=200,default='Not set yet')
    last_used = DateTimeField(default=datetime.now())
    created_on = DateTimeField(default=datetime.now())
    state = StringField(max_length=300,default='Ready')
    owner = StringField(max_length=100,default='no')



#The below is to avoid the error occue when importing Repo from autoncore because of the User class which cases the error
try:    
    from mongoengine.django.auth import User
    class OUser(User):
        repos = ListField(ReferenceField(Repo),unique=True,required=False)

except:
    pass


