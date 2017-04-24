import os
import string
import random
from OnToology.models import *

user_password = os.environ['test_user_token']


def delete_all_repos():
    for u in OUser.objects.all():
        u.repos = []
        u.save()
    Repo.objects.delete()


def create_repo(url='ahmad88me/demo', user=None):
    r = Repo(url=url)
    r.save()
    if user is None:
        user = OUser.objects.all()[0]
    user.repos.append(r)
    user.save()


def create_user():
    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
    user = OUser()
    user.email = os.environ['test_user_email']
    user.username = user.email
    user.password = os.environ['test_user_token']
    user.token = sec
    user.save()


def delete_all_publishnames():
    PublishName.objects.delete()


def create_publishname(name=None, user=None, repo=None, ontology=None):
    if name is None or user is None or repo is None or ontology is None:
        print "Error, cannot create a publishname, missing parameters"
        raise Exception('in create publishname, missing parameters')
    pn = PublishName(name=name, user=user, repo=repo, ontology=ontology)
    pn.save()