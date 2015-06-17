from mongoengine import Document,StringField,DateTimeField,ListField,ReferenceField, BooleanField
#from mongoengine.django.auth import User
from datetime import datetime





class Repo(Document):
    url = StringField(max_length=200,default='Not set yet')
    last_used = DateTimeField(default=datetime.now())
    state = StringField(max_length=300,default='Ready')
    owner = StringField(max_length=100,default='no')
    previsual = BooleanField(default=False)
    previsual_page_available = BooleanField(default=False)



#The below is to avoid the error occue when importing Repo from autoncore because of the User class which cases the error
try:    
    from mongoengine.django.auth import User
    class OUser(User):
        repos = ListField(ReferenceField(Repo))

except:
    pass


