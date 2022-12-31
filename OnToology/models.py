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
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.models import AbstractUser as User
from django.db import models
from datetime import datetime, timedelta


class Repo(models.Model):
    url = models.CharField(max_length=200, default='Not set yet')
    last_used = models.DateTimeField(default=timezone.now)
    state = models.CharField(max_length=300, default='Ready')
    notes = models.TextField(default='')
    progress = models.FloatField(default=0.0)

    def json(self):
        return {
            "id": str(self.id),
            "url": self.url,
            "last_used": self.last_used.strftime('%Y-%m-%d %H:%M'),
            "state": self.state,
            "notes": self.notes,
        }

    def update_ontology_status(self, ontology, status):
        print("in update ontology status all")
        print("ontology: <"+ontology+">"+" status: <"+status+">")
        # for osp in self.ontology_status_pairs.all():
        for osp in OntologyStatusPair.objects.filter(repo=self):
            print("in for: ")
            # print(osp)
            print("name: "+osp.name)
            if osp.name == ontology:
                print("The status of %s is updated" % osp.name)
                osp.status = status
                osp.save()
                return True
        print("stage 4")
        osp = OntologyStatusPair(name=ontology, status=status, repo=self)
        osp.save()
        print("stage final")

    def clear_ontology_status_pairs(self):
        print("clear ontology status pairs for repo: "+self.url)
        OntologyStatusPair.objects.filter(repo=self).delete()
        # for osp in self.ontology_status_pairs.all():
        #     self.ontology_status_pairs.remove(osp)
        # self.ontology_status_pairs.clear()
        self.save()

    def __unicode__(self):
        return self.url


def tomorrow_exp():
    d = timezone.now()
    return d + timedelta(days=1)


class OUser(AbstractBaseUser):
    repos = models.ManyToManyField(Repo, related_name="ousers")
    # repos = models.ArrayReferenceField(to=Repo, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)  # The permission access level to OnToology
    token = models.TextField(default='no token')
    token_expiry = models.DateTimeField(default=tomorrow_exp)

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(verbose_name='user name', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.username

    # Maybe required?
    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def json(self):
        return {'id': str(self.id),
                'private': self.private,
                'email': self.email}

    def __unicode__(self):
        return self.username


class OntologyStatusPair(models.Model):
    STATUSES = (
        ('pending', 'pending'),
        ('diagram', 'diagram'),
        ('documentation', 'documentation'),
        ('evaluation', 'evaluation'),
        ('jsonld', 'jsonld'),
        ('validation', 'validation'),
        ('finished', 'finished')
    )
    name = models.CharField(max_length=120)
    status = models.CharField(max_length=25, choices=STATUSES)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE, related_name='ontology_status_pairs')

    def json(self):
        return {
            "name": self.name,
            "status": self.status
        }

    def __unicode__(self):
        return self.name + ' - ' + self.status


class PublishName(models.Model):
    name = models.TextField()
    user = models.ForeignKey(OUser, on_delete=models.CASCADE, related_name='publishnames')
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE, related_name='publishnames')
    ontology = models.TextField(default='')

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


class ORun(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE, related_name='oruns')
    branch = models.TextField(default='')
    user = models.ForeignKey(OUser, on_delete=models.CASCADE, related_name='oruns')
    timestamp = models.DateTimeField(default=timezone.now)
    # tasks = models.EmbeddedField(model_container=OTask)
    # tasks = models.ArrayReferenceField(OTask, on_delete=models.CASCADE)

    def __unicode__(self):
        return "run <"+str(self.id)+"> " + self.user.email + " - " + self.repo.url + " - " + str(self.timestamp)


class OTask(models.Model):
    name = models.TextField()
    description = models.TextField()
    success = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    orun = models.ForeignKey(ORun, on_delete=models.CASCADE, related_name='otasks')

