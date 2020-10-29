import os
import string
import random
from OnToology.models import *
from subprocess import call

user_password = os.environ['test_user_token']


def delete_all_repos_from_db():
    for u in OUser.objects.all():
        u.repos = []
        u.save()
    for r in Repo.objects.all():
        r.delete()
        r.save()
    Repo.objects.all().delete()


def delete_all_users():
    for u in OUser.objects.all():
        u.delete()
        u.save()
    OUser.objects.all().delete()


def create_repo(url=None, user=None):
    r = Repo(url=url)
    r.save()
    if user is None:
        user = OUser.objects.all()[0]
    user.repos.add(r)
    user.save()
    return r


def create_user():
    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
    user = OUser.objects.create_user(email=os.environ['test_user_email'], username=os.environ['test_user_email'],
                             password=os.environ['test_user_token'], token=sec)
    # user = OUser()
    # user.email = os.environ['test_user_email']
    # user.username = user.email
    # user.password = os.environ['test_user_token']
    # user.token = sec
    # user.save()


def delete_all_publishnames():
    PublishName.objects.delete()


def create_publishname(name=None, user=None, repo=None, ontology=None):
    if name is None or user is None or repo is None or ontology is None:
        print("Error, cannot create a publishname, missing parameters")
        raise Exception('in create publishname, missing parameters')
    pn = PublishName(name=name, user=user, repo=repo, ontology=ontology)
    pn.save()


def get_repo_resource_dir(user_email):
    """
    get absolute dir of the resources (OnToology) folder (e.g. /home/user/repos/a@b.com/OnToology)
    :param user_email:
    :return:
    """
    base_dir = os.path.join(os.environ['github_repos_dir'], user_email)
    from Integrator import config_folder_name
    abs_path = os.path.join(base_dir, config_folder_name)
    return abs_path


def clone_if_not(resources_dir, repo):
    repo_dir = os.path.join(resources_dir, os.pardir)
    repo_dir = os.sep.join(resources_dir.split(os.sep)[:-1])
    if not os.path.isdir(repo_dir):
        cloning_url = "git@github.com:%s.git" % repo.strip()
        comm = "git clone --recurse-submodules  " + cloning_url + " " + repo_dir
        print("comm: %s" % comm)
        call(comm, shell=True)


