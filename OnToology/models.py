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


from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, BooleanField, FloatField
# from mongoengine.django.auth import User
from datetime import datetime, timedelta


class OntologyStatusPair(Document):
    STATUSES = (
        ('documentation', 'documentation'),
        ('diagram', 'diagram'),
        ('evaluation', 'evaluation'),
        ('jsonld', 'jsonld'),
        ('pending', 'pending'),
        ('finished', 'finished')
    )
    name = StringField(max_length=120)
    status = StringField(choices=STATUSES)

    def json(self):
        return {
            "name": self.name,
            "status": self.status
        }

    def __unicode__(self):
        return self.name + ' - ' + self.status


class Repo(Document):
    url = StringField(max_length=200, default='Not set yet')
    last_used = DateTimeField(default=datetime.now())
    state = StringField(max_length=300, default='Ready')
    owner = StringField(max_length=100, default='no')
    previsual = BooleanField(default=False)
    previsual_page_available = BooleanField(default=False)
    notes = StringField(default='')
    progress = FloatField(default=0.0)
    ontology_status_pairs = ListField(ReferenceField(OntologyStatusPair), default=[])

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

    def __unicode__(self):
        return self.url

# The below is to avoid the error occur when importing Repo from autoncore because of the User class which cases the
# error
try:    
    from mongoengine.django.auth import User

    class OUser(User):
        repos = ListField(ReferenceField(Repo))
        private = BooleanField(default=False)  # The permission access level to OnToology
        token = StringField(default='no token')
        token_expiry = DateTimeField(default=datetime.now()+timedelta(days=1))

        def json(self):
            return {'id': str(self.id),
                    'private': self.private,
                    'email': self.email}

        def __unicode__(self):
            return self.username


    class PublishName(Document):
        name = StringField()
        user = ReferenceField(OUser)
        repo = ReferenceField(Repo)
        ontology = StringField(default='')

        def json(self):
            return {
                    'id': str(self.id),
                    'name': self.name,
                    'user': self.user.json(),
                    'repo': self.repo.json(),
                    'ontology': self.ontology
                    }

        def __unicode__(self):
            return self.name
except:
    pass



