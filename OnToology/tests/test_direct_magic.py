import json
import string
import random
import shutil
import os
from subprocess import call
from .api_util import create_user, create_repo, delete_all_repos_from_db, get_repo_resource_dir, clone_if_not, delete_all_users
from .api_util import prepare_resource_dir, PrintLogger
import logging
from multiprocessing import Process
from django.test import Client
from unittest import TestCase
from django.test.testcases import SerializeMixin
from OnToology.models import OUser, Repo
from OnToology import sqclient
from time import sleep
from .serializer import Serializer


queue_name = 'ontoology'


def get_logger(name, logdir="", level=logging.INFO):
    # logging.basicConfig(level=level)
    logger = logging.getLogger(name)
    if logdir != "":
        handler = logging.FileHandler(logdir)
    else:
        handler = logging.StreamHandler()
    #
    # handler = logging.FileHandler('property-output.log')
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


logger = PrintLogger()


def get_pending_messages():
    return sqclient.get_pending_messages()


class TestDirectMagic(Serializer, TestCase):
    def setUp(self):
        print("setup DirectMagic")
        delete_all_users()
        delete_all_repos_from_db()
        # if len(OUser.objects.all()) == 0:
        #     create_user()
        create_user()
        self.url = 'ahmad88me/ontoology-auto-test-no-res'
        self.user = OUser.objects.all()[0]

        num_of_msgs = get_pending_messages()
        logger.debug("test> number of messages in the queue is: " + str(num_of_msgs))

    def test_generate_all_slash_direct_but_doc(self):
        print("\n\n###################### test_generate_all_slash_direct_but_doc ###############\n\n")
        logger.error("testing the logger\n\n\n\n\n")
        resources_dir = get_repo_resource_dir(os.environ['test_user_email'])
        clone_if_not(resources_dir, self.url)
        # The below two assertion is to protect the deletion of important files
        self.assertEqual(resources_dir.split('/')[-1], 'OnToology', msg='might be a wrong resources dir OnToology')
        self.assertIn(os.environ['test_user_email'], resources_dir, msg='might be a wrong resources dir or wrong user')
        print("will delete %s" % resources_dir)
        comm = "rm -Rf %s" % resources_dir
        print(comm)
        call(comm, shell=True)
        prepare_resource_dir(resources_dir, 'alo.owl')
        prepare_resource_dir(resources_dir, 'geolinkeddata.owl')

        create_repo(url=self.url, user=self.user)

        # inject the configuration file
        conf_path = os.path.join(resources_dir, 'alo.owl', 'OnToology.cfg')
        print("Inject conf: %s" % conf_path)
        f = open(conf_path, 'w')
        conf_file_content = """
[ar2dtool]
enable = True

[widoco]
enable = False
languages = en,es,it
webVowl = False

[oops]
enable = True

[owl2jsonld]
enable = True
                """
        f.write(conf_file_content)
        f.close()

        # inject the configuration file with the multi-lang
        conf_path = os.path.join(resources_dir, 'geolinkeddata.owl', 'OnToology.cfg')
        print("Inject conf: %s" % conf_path)
        f = open(conf_path, 'w')
        conf_file_content = """
[ar2dtool]
enable = False

[widoco]
enable = False
languages = en,es,it
webVowl = False

[oops]
enable = False

[owl2jsonld]
enable = False
                        """
        f.write(conf_file_content)
        f.close()

        logger.debug("pre API> number of messages count: " + str(get_pending_messages()))
        j = {
            "repo": self.url,
            "useremail": self.user.email,
            "changedfiles": ["alo.owl", ],
            "branch": "master",
            "action": "magic"
        }
        sqclient.handle_action(j, logger, raise_exp=True)
        self.assertEqual(1, len(Repo.objects.all()))
        repo = Repo.objects.all()[0]

        files_to_check = ['alo.owl/OnToology.cfg',]
        docs_files = ['index-en.html', 'ontology.xml', '.htaccess', 'alo.owl.widoco.conf']
        diagrams_files = ['ar2dtool-class/alo.owl.png', 'ar2dtool-taxonomy/alo.owl.png']

        print("\nStarting the test block\n")

        # Test block
        cmd_p = os.path.join(resources_dir, files_to_check[0])
        logger.debug(cmd_p)
        cmd_pp = "/".join(cmd_p.split("/")[:-1])
        logger.debug(cmd_pp)
        cmd = "ls -ltra " + cmd_pp
        logger.debug("\n\n cmd: "+cmd)
        stream = os.popen(cmd)
        output = stream.read()
        logger.debug(output)

        # os.system(cmd)
        eval_files = ['oops.html']
        # for f in docs_files:
        #     ff = os.path.join('alo.owl/documentation', f)
        #     files_to_check.append(ff)
        for f in diagrams_files:
            ff = os.path.join('alo.owl/diagrams', f)
            files_to_check.append(ff)
        for f in eval_files:
            ff = os.path.join('alo.owl/evaluation', f)
            files_to_check.append(ff)
        for f in files_to_check:
            print(os.path.join(resources_dir, f))
            self.assertTrue(os.path.exists(os.path.join(resources_dir, f)), msg=(f+" does not exists"))
        delete_all_repos_from_db()
        # p.terminate()
        print("-------------\n\n\n---------- test_generate_all_check_generated_resources_slash ###############\n\n")
