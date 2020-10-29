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
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, UserManager
from django.contrib.auth.models import AbstractUser as User
from djongo import models

from datetime import datetime, timedelta


# class CustomUserManager(BaseUserManager):
#
#     def create_user(self, email, username, password=None, ):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user


# class CustomUser(AbstractBaseUser):
#     email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
#     username = models.CharField(verbose_name='user name', max_length=255, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     objects = UserManager()
#     # objects = CustomUserManager()
#
#     USERNAME_FIELD = 'username'
#     # REQUIRED_FIELDS = ['date_of_birth']
#
#     def __str__(self):
#         return self.email
#
#     # Maybe required?
#     def get_group_permissions(self, obj=None):
#         return set()
#
#     def get_all_permissions(self, obj=None):
#         return set()
#
#     def has_perm(self, perm, obj=None):
#         return True
#
#     def has_perms(self, perm_list, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True

    # Admin required fields
    # @property
    # def is_staff(self):
    #     return self.is_admin


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

    def json(self):
        return {
            "name": self.name,
            "status": self.status
        }

    def __unicode__(self):
        return self.name + ' - ' + self.status




class Repo(models.Model):
    url = models.CharField(max_length=200, default='Not set yet')
    last_used = models.DateTimeField(default=timezone.now)
    state = models.CharField(max_length=300, default='Ready')
    branch = models.TextField(default="master")
    previsual = models.BooleanField(default=False)
    previsual_page_available = models.BooleanField(default=False)
    notes = models.TextField(default='')
    progress = models.FloatField(default=0.0)
    ontology_status_pairs = models.ArrayReferenceField(OntologyStatusPair, on_delete=models.CASCADE)
    busy = models.BooleanField(default=False)  # backward compatibility

    def json(self):
        return {
            "id": str(self.id),
            "url": self.url,
            "last_used": self.last_used.strftime('%Y-%m-%d %H:%M'),
            "state": self.state,
            "previsual": self.previsual,
            "previsual_page_available": self.previsual_page_available,
            "notes": self.notes,
        }

    def update_ontology_status(self, ontology, status):
        print("in update ontology status all")
        print("ontology: <"+ontology+">"+" status: <"+status+">")
        for osp in self.ontology_status_pairs.all():
            print("in for: ")
            # print(osp)
            print("name: "+osp.name)
            if osp.name == ontology:
                print("The status of %s is updated" % osp.name)
                osp.status = status
                osp.save()
                return True
        print("stage 4")
        osp = OntologyStatusPair(name=ontology, status=status)
        osp.save()
        print("stage 5")
        self.ontology_status_pairs.add(osp)
        print("stage 6")
        self.save()
        print("stage final")

    def clear_ontology_status_pairs(self):
        print("clear ontology status pairs for repo: "+self.url)
        for osp in self.ontology_status_pairs.all():
            self.ontology_status_pairs.remove(osp)
        # self.ontology_status_pairs.clear()
        self.save()

    def __unicode__(self):
        return self.url


def tomorrow_exp():
    d = timezone.now()
    return d + timedelta(days=1)


class OUser(AbstractBaseUser):
    repos = models.ArrayReferenceField(to=Repo, on_delete=models.CASCADE)
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
    #objects = CustomUserManager()

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


class PublishName(models.Model):
    name = models.TextField()
    user = models.ForeignKey(OUser, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
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


class OTask(models.Model):
    name = models.TextField()
    description = models.TextField()
    success = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    # class Meta:
    #     abstract = True


class ORun(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    user = models.ForeignKey(OUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    # tasks = models.EmbeddedField(model_container=OTask)
    tasks = models.ArrayReferenceField(OTask, on_delete=models.CASCADE)

    def __unicode__(self):
        return "run <"+str(self.id)+"> " + self.user.email + " - " + self.repo.url + " - " + str(self.timestamp)



