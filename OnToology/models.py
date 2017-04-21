#
# Copyright 2012-2013 Ontology Engineering Group, Universidad Politecnica de Madrid, Spain
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @author Ahmad Alobaid
#


from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, BooleanField
# from mongoengine.django.auth import User
from datetime import datetime, timedelta


class Repo(Document):
    url = StringField(max_length=200, default='Not set yet')
    last_used = DateTimeField(default=datetime.now())
    state = StringField(max_length=300, default='Ready')
    owner = StringField(max_length=100, default='no')
    previsual = BooleanField(default=False)
    previsual_page_available = BooleanField(default=False)
    notes = StringField(default='')

    def json(self):
        return {
            "id": str(self.id),
            "url": self.url,
            "last_used": self.last_used.strftime('%Y-%m-%d %H:%M'),
            "state": self.state,
            "owner": self.owner,
            "previsual": self.previsual,
            "previsual_page_available": self.previsual_page_available,
            "notes": self.notes
        }


# The below is to avoid the error occue when importing Repo from autoncore because of the User class which cases the
# error
try:    
    from mongoengine.django.auth import User

    class OUser(User):
        repos = ListField(ReferenceField(Repo))
        private = BooleanField(default=False)  # The permission access level to OnToology
        token = StringField(default='no token')
        token_expiry = DateTimeField(default=datetime.now()+timedelta(days=1))


    class PublishName(Document):
        name = StringField()
        user = ReferenceField(OUser)
        repo = ReferenceField(Repo)
        ontology = StringField(default='')

except:
    pass



