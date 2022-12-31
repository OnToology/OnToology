import os
import string
import shutil
import random
from OnToology.models import OUser, Repo
from subprocess import call

user_password = os.environ['test_user_token']


class PrintLogger():

    def error(self, msg):
        print(msg)

    def debug(self, msg):
        print(msg)

    def info(self, msg):
        print(msg)


def delete_all_repos_from_db():
    Repo.objects.all().delete()


def delete_all_users():
    OUser.objects.all().delete()


def create_repo(url=None, user=None):
    if user is None:
        print("user is none")
        user = OUser.objects.all()[0]
    else:
        print("user is passed")
        print(type(user))
        print(user.json())
    print(OUser.objects.all())
    print(Repo.objects.all())
    r = Repo(url=url)
    r.save()
    user.repos.add(r)
    user.save()
    return r


def create_user():
    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
    user = OUser.objects.create_user(email=os.environ['test_user_email'], username=os.environ['test_user_email'],
                             password=os.environ['test_user_token'], token=sec)
    user.save()


def delete_all_publishnames():
    PublishName.objects.all().delete()


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
    repo_dir = os.sep.join(resources_dir.split(os.sep)[:-1])
    if not os.path.exists(resources_dir):
        cloning_url = "git@github.com:%s.git" % repo.strip()
        comm = "git clone --recurse-submodules  " + cloning_url + " " + repo_dir
        print("comm: %s" % comm)
        call(comm, shell=True)


def prepare_resource_dir(resources_dir, fname):
    """
    If the setup is not to clone a fresh copy then check if it exists. If not, then create the necessary dir
    :param resources_dir: <>/OnToology/fname
    :param fname: e.g., alo.owl
    :return:
    """
    if not os.path.exists(resources_dir):
        os.mkdir(resources_dir)
    ontology_dir = os.path.join(resources_dir, fname)
    if os.path.exists(ontology_dir):
        shutil.rmtree(ontology_dir)
    os.mkdir(ontology_dir)

