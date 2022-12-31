import string
import random
import os
from subprocess import call
from .api_util import create_user, delete_all_repos_from_db, delete_all_users
from .api_util import get_repo_resource_dir
from OnToology import autoncore
from unittest import TestCase
from OnToology.models import OUser, Repo
from .serializer import Serializer
import Integrator


class TestDirectConf(Serializer, TestCase):

    def setUp(self):
        print("setup DirectMagicConf")
        delete_all_users()
        delete_all_repos_from_db()
        create_user()

        self.url_original_case = 'ahmad88me/Test-ontoology-Demo'
        self.url_lower_case = self.url_original_case.lower()
        self.user = OUser.objects.all()[0]
        self.cloning_url = 'git@github.com:%s.git' % self.url_lower_case

    def test_create_new_conf(self):
        """
        :return:
        """
        cloning_url = self.cloning_url
        sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
        folder_name = 'newconf-' + sec
        # delete the folder if it exists
        comm = "rm" + " -Rf " + os.path.join(autoncore.home, folder_name)
        print(comm)
        call(comm, shell=True)
        abs_repo_dir = autoncore.clone_repo(cloning_url, folder_name, dosleep=True, branch="main")
        self.assertTrue(os.path.exists(os.path.join(abs_repo_dir, "ALo", "aLo.owl")))
        self.assertTrue(os.path.exists(os.path.join(abs_repo_dir, "GeO", "geoLinkedData.owl")))
        self.assertFalse(os.path.exists(os.path.join(abs_repo_dir, "OnToology", "ALo", "aLo.owl")))
        self.assertFalse(os.path.exists(os.path.join(abs_repo_dir, "OnToology", "GeO", "geoLinkedData.owl")))
        Integrator.create_of_get_conf(os.path.join("ALo", "aLo.owl"), abs_repo_dir)
        Integrator.create_of_get_conf(os.path.join("GeO", "geoLinkedData.owl"), abs_repo_dir)
        self.assertTrue(os.path.exists(os.path.join(abs_repo_dir, "OnToology", "ALo", "aLo.owl", "OnToology.cfg")))
        self.assertTrue(
            os.path.exists(os.path.join(abs_repo_dir, "OnToology", "GeO", "geoLinkedData.owl", "OnToology.cfg")))
        t_alo = open(os.path.join(abs_repo_dir, "OnToology", "ALo", "aLo.owl", "OnToology.cfg")).read()
        t_geo = open(os.path.join(abs_repo_dir, "OnToology", "GeO", "geoLinkedData.owl", "OnToology.cfg")).read()
        self.assertFalse(t_alo.strip() == "")
        self.assertFalse(t_geo.strip() == "")

    def test_widoco_lang_conf(self):
        sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
        folder_name = 'newconf-wlang-' + sec
        # delete the folder if it exists
        comm = "rm" + " -Rf " + os.path.join(autoncore.home, folder_name)
        print(comm)
        call(comm, shell=True)
        abs_repo_dir = autoncore.clone_repo(self.cloning_url, folder_name, dosleep=True, branch="main")
        self.assertTrue(os.path.exists(os.path.join(abs_repo_dir, "ALo", "aLo.owl")))
        self.assertTrue(os.path.exists(os.path.join(abs_repo_dir, "GeO", "geoLinkedData.owl")))
        self.assertFalse(os.path.exists(os.path.join(abs_repo_dir, "OnToology", "ALo", "aLo.owl")))
        self.assertFalse(os.path.exists(os.path.join(abs_repo_dir, "OnToology", "GeO", "geoLinkedData.owl")))
        conf_content = """
[owl2jsonld]
enable = false

[widoco]
enable = true
webvowl = false
languages = en,es

[themis]
enable = false

[ar2dtool]
enable = false

[oops]
enable = false

"""
        Integrator.create_of_get_conf(os.path.join("ALo", "aLo.owl"), abs_repo_dir)
        conf_file_abs_alo = os.path.join(abs_repo_dir, "OnToology", "ALo", "aLo.owl", "OnToology.cfg")
        f = open(conf_file_abs_alo, 'w')
        f.write(conf_content)
        f.close()

        conf_alo = Integrator.create_of_get_conf(os.path.join("ALo", "aLo.owl"), abs_repo_dir)
        print(conf_alo)
        self.assertListEqual(["en", "es"], conf_alo.getlist('widoco', 'languages'))

    def test_fix_old_conf(self):
        """
        :return:
        """
        sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
        folder_name = 'fix-old-conf-' + sec
        # delete the folder if it exists
        comm = "rm" + " -Rf " + os.path.join(autoncore.home, folder_name)
        print(comm)
        call(comm, shell=True)
        abs_repo_dir = autoncore.clone_repo(self.cloning_url, folder_name, dosleep=True, branch="main")
        self.assertTrue(os.path.exists(os.path.join(abs_repo_dir, "ALo", "aLo.owl")))
        self.assertTrue(os.path.exists(os.path.join(abs_repo_dir, "GeO", "geoLinkedData.owl")))
        self.assertFalse(os.path.exists(os.path.join(abs_repo_dir, "OnToology", "ALo", "aLo.owl")))
        self.assertFalse(os.path.exists(os.path.join(abs_repo_dir, "OnToology", "GeO", "geoLinkedData.owl")))
        conf_content = """
[widoco]
enable = false

[ar2dtool]
enable = false

[oops]
enable = false

        """
        conf_alo = Integrator.create_of_get_conf(os.path.join("ALo", "aLo.owl"), abs_repo_dir)
        conf_file_abs_alo = os.path.join(abs_repo_dir, "OnToology", "ALo", "aLo.owl", "OnToology.cfg")
        f = open(conf_file_abs_alo, 'w')
        f.write(conf_content)
        f.close()

        self.assertListEqual(["en"], conf_alo.getlist('widoco', 'languages'))
        self.assertTrue(conf_alo.has_section('themis'))
