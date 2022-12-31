import json
import string
import random
import os
from subprocess import call
from .api_util import create_user, create_repo, delete_all_repos_from_db, get_repo_resource_dir, clone_if_not
from .api_util import delete_all_users, prepare_resource_dir
import logging

from multiprocessing import Process
from django.test import Client
from unittest import TestCase
from .serializer import Serializer
from OnToology.models import OUser, Repo
from OnToology import sqclient
from time import sleep


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


logger = get_logger(__name__, level=logging.DEBUG)

#
#
# def set_config(logger, logdir=""):
#     """
#     :param logger: logger
#     :param logdir: the directory log
#     :return:
#     """
#     if logdir != "":
#         handler = logging.FileHandler(logdir)
#     else:
#         handler = logging.StreamHandler()
#     formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     logger.setLevel(logging.DEBUG)
#     return logger
#
#
# logger = logging.getLogger(__name__)
# logger = set_config(logger)


def get_pending_messages():
    return sqclient.get_pending_messages()


class TestActionAPIs(Serializer, TestCase):

    def setUp(self):
        print("setup TestActionAPIs")
        delete_all_users()
        if len(OUser.objects.all()) == 0:
            create_user()
        else:
            print("Not all users where deleted")
            raise Exception("Error deleteing users")
        self.url = 'ahmad88me/ontoology-auto-test-no-res'
        self.user = OUser.objects.all()[0]
        self.branch = 'master'
        num_of_msgs = get_pending_messages()
        logger.debug("test> number of messages in the queue is: " + str(num_of_msgs))
        delete_all_repos_from_db()

    def test_generate_all_check_generated_resources_slash(self):
        print("###############\n\n\n\n\n##########test_generate_all_check_generated_resources_slash###############\n\n")
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
        print("number of repos before deleting: "+str(len(Repo.objects.all())))
        print("number of users: "+str(len(OUser.objects.all())))
        print("user repos: ")
        print(OUser.objects.all()[0].repos)
        delete_all_repos_from_db()
        print("number of repos after deleting: "+str(len(Repo.objects.all())))
        print("number of users: "+str(len(Repo.objects.all())))
        print(OUser.objects.all()[0].repos)
        create_repo(url=self.url, user=self.user)
        print("number of repos after creating a new one: "+str(len(Repo.objects.all())))
        print("number of users: "+str(len(Repo.objects.all())))
        print(OUser.objects.all()[0].repos)

        # # If the setup is not to clone a fresh copy then check if it exists, if not then clone
        # if not os.path.exists(resources_dir):
        #     os.mkdir(resources_dir)
        # ontology_dir = os.path.join(resources_dir, 'alo.owl')
        # if os.path.exists(ontology_dir):
        #     shutil.rmtree(ontology_dir)
        # os.mkdir(ontology_dir)
        #
        # ontology_dir = os.path.join(resources_dir, 'geolinkeddata.owl')
        # if os.path.exists(ontology_dir):
        #     shutil.rmtree(ontology_dir)
        # os.mkdir(ontology_dir)

        # inject the configuration file
        f = open(os.path.join(resources_dir, 'alo.owl/OnToology.cfg'), 'w')
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
        f = open(os.path.join(resources_dir, 'geolinkeddata.owl/OnToology.cfg'), 'w')
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
        c = Client()
        print("printing repo: ")
        print(Repo.objects.all()[0].json())
        curr_num = get_pending_messages()
        response = c.post('/api/generate_all', {'url': Repo.objects.all()[0].url, 'branch': self.branch},
                          HTTP_AUTHORIZATION='Token '+self.user.token)
        print("---------------\n\n\n\n\n--- IN THE MIDDLE --test_generate_all_check_generated_resources_slash###############\n\n")
        self.assertEqual(response.status_code, 202, msg=response.content)
        print("post API> number of messages count: " + str(get_pending_messages()))
        logger.debug("post API> number of messages count: " + str(get_pending_messages()))
        # p = Process(target=start_pool)
        # p.start()
        logger.debug("process spawn> number of messages count: " + str(get_pending_messages()))
        while get_pending_messages() > curr_num:
            logger.debug("while> number of messages count: "+str(get_pending_messages()))
            print("while> number of messages count: "+str(get_pending_messages()))
            sleep(3)
        logger.debug("after while> should be executed "+str(get_pending_messages()))
        print("after while> should be executed "+str(get_pending_messages()))

        self.assertEqual(1, len(Repo.objects.all()))
        repo = Repo.objects.all()[0]
        while repo.state != 'Ready':
            sleep(2)
            logger.debug('wait> status: '+repo.state)
            logger.debug('notes: '+repo.notes)
            print('wait> status: '+repo.state)
            print('notes: '+repo.notes)

            repo = Repo.objects.all()[0]

        files_to_check = ['alo.owl/OnToology.cfg',]
        diagrams_files = ['ar2dtool-class/alo.owl.png', 'ar2dtool-taxonomy/alo.owl.png']

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
        print("---------------\n\n\n\n\n----------test_generate_all_check_generated_resources_slash###############\n\n")

    def test_generate_all_check_generated_resources_hash(self):
        print("###############\n\n\n\n\n##########test_generate_all_check_generated_resources_hash###############\n\n")
        resources_dir = get_repo_resource_dir(self.user.email)
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
        delete_all_repos_from_db()
        create_repo(url=self.url, user=self.user)
        c = Client()
        # inject the configuration file with the multi-lang
        f = open(os.path.join(resources_dir, 'geolinkeddata.owl/OnToology.cfg'), 'w')
        conf_file_content = """
[ar2dtool]
enable = True

[widoco]
enable = False
languages = en,es,it
webVowl = False

[oops]
enable = False

[owl2jsonld]
enable = True
                        """
        f.write(conf_file_content)
        f.close()

        # inject the configuration file
        f = open(os.path.join(resources_dir, 'alo.owl/OnToology.cfg'), 'w')
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

        print("url repo ")
        print("\n\n\n\nnum of repos %d" % len(Repo.objects.all()))
        logger.debug("\n\n\n\nnum of repos %d" % len(Repo.objects.all()))
        print("url repo url: "+Repo.objects.all()[0].url)
        response = c.post('/api/generate_all', {'url': Repo.objects.all()[0].url, 'branch': self.branch},
                          HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 202, msg=response.content)
        sleep(3)
        repo = Repo.objects.all()[0]

        while repo.state != 'Ready':
            sleep(2)
            logger.debug('wait> status: '+repo.state)
            logger.debug('notes: '+repo.notes)
            print('wait> status: '+repo.state)
            print('notes: '+repo.notes)

            repo = Repo.objects.all()[0]

        files_to_check = ['geolinkeddata.owl/OnToology.cfg', ]
        diagrams_files = ['ar2dtool-class/geolinkeddata.owl.png', 'ar2dtool-taxonomy/geolinkeddata.owl.png']
        eval_files = ['oops.html']
        # for f in docs_files:
        #     ff = os.path.join('geolinkeddata.owl/documentation', f)
        #     files_to_check.append(ff)
        for f in diagrams_files:
            ff = os.path.join('geolinkeddata.owl/diagrams', f)
            files_to_check.append(ff)
        # Because oops APIs at the moment gives an error for this ontology
        # for f in eval_files:
        #     ff = os.path.join('geolinkeddata.owl/evaluation', f)
        #     files_to_check.append(ff)
        for f in files_to_check:
            print(os.path.join(resources_dir, f))
            self.assertTrue(os.path.exists(os.path.join(resources_dir, f)), msg=(str(f) + " does not exists."))
        delete_all_repos_from_db()


















#     def test_doc_multi_lang(self):
#         return
#         print("###############\n\n\n\n\n##########test_doc_multi_lang###############\n\n")
#         import OnToology.settings as settings
#         resources_dir = get_repo_resource_dir(os.environ['test_user_email'])
#         print("resources dir: <%s>" % resources_dir)
#         # The below two assertion is to protect the deletion of important files
#         self.assertEqual(resources_dir.split('/')[-1], 'OnToology', msg='might be a wrong resources dir OnToology')
#         self.assertIn(os.environ['test_user_email'], resources_dir, msg='might be a wrong resources dir or wrong user')
#         # print "will delete %s" % resources_dir
#         # comm = "rm -Rf %s" % resources_dir
#         # print comm
#         settings.test_conf['local'] = True
#         settings.test_conf['fork'] = False
#         settings.test_conf['clone'] = False
#         settings.test_conf['push'] = False
#         settings.test_conf['pull'] = False
#         delete_all_repos_from_db()
#         print("to create repo")
#         create_repo(url=self.url, user=self.user)
#         print("repo is created")
#         self.assertEqual(1, len(Repo.objects.all()))
#
#         # If the setup is not to clone a fresh copy then check if it exists, if not then clone
#         if settings.test_conf['clone'] is False:
#             clone_if_not(resources_dir, self.url)
#         if not os.path.exists(resources_dir):
#             os.mkdir(resources_dir)
#         ontology_dir = os.path.join(resources_dir, 'alo.owl')
#         if os.path.exists(ontology_dir):
#             shutil.rmtree(ontology_dir)
#         os.mkdir(ontology_dir)
#
#         ontology_dir = os.path.join(resources_dir, 'geolinkeddata.owl')
#         if os.path.exists(ontology_dir):
#             shutil.rmtree(ontology_dir)
#         os.mkdir(ontology_dir)
#
#         # inject the configuration file with the multi-lang
#         f = open(os.path.join(resources_dir, 'alo.owl/OnToology.cfg'), 'w')
#         conf_file_content="""
# [ar2dtool]
# enable = False
#
# [widoco]
# enable = True
# languages = en,es,it
# webVowl = False
#
# [oops]
# enable = False
#
# [owl2jsonld]
# enable = False
#         """
#         f.write(conf_file_content)
#         f.close()
#
#         # inject the configuration file with the multi-lang
#         f = open(os.path.join(resources_dir, 'geolinkeddata.owl/OnToology.cfg'), 'w')
#         conf_file_content = """
# [ar2dtool]
# enable = False
#
# [widoco]
# enable = True
# languages = en,es,it
# webVowl = False
#
# [oops]
# enable = False
#
# [owl2jsonld]
# enable = False
#         """
#         f.write(conf_file_content)
#         f.close()
#
#         c = Client()
#         print("JUST before calling the api\n")
#         response = c.post('/api/generate_all', {'url': Repo.objects.all()[0].url},
#                           HTTP_AUTHORIZATION='Token '+self.user.token)
#         self.assertEqual(response.status_code, 202, msg=response.content)
#         print("response: "+str(response.content))
#         logger.debug("Response: "+str(response.content))
#         # p = Process(target=start_pool)
#         # p.start()
#
#         self.assertEqual(1, len(Repo.objects.all()))
#         logger.debug("process spawn> number of messages count: " + str(get_pending_messages()))
#         while get_pending_messages()>0:
#             logger.debug("while> number of messages count: "+str(get_pending_messages()))
#         logger.debug("after while> should be executed "+str(get_pending_messages()))
#
#         repo = Repo.objects.all()[0]
#         while repo.state != 'Ready':
#             sleep(2)
#             print("waiting> status: "+repo.state)
#             logger.debug('wait> status: '+repo.state)
#             logger.debug('notes: '+repo.notes)
#             repo = Repo.objects.all()[0]
#
#         files_to_check = ['alo.owl/OnToology.cfg', 'geolinkeddata.owl/OnToology.cfg']
#         docs_files_ = ['index-en.html', 'index-es.html', 'index-it.html', 'ontology.xml']
#         docs_files_geo = docs_files_
#         docs_files_alo = docs_files_ + ['alo.owl.widoco.conf', '.htaccess']
#
#         # Test block
#         cmd_p = os.path.join(resources_dir, files_to_check[0])
#         logger.debug(cmd_p)
#         cmd_pp = "/".join(cmd_p.split("/")[:-1])
#         logger.debug(cmd_pp)
#         cmd = "ls -ltra " + cmd_pp
#         logger.debug("\n\n cmd: "+cmd)
#         stream = os.popen(cmd)
#         output = stream.read()
#         logger.debug(output)
#
#
# #        docs_files_alo = ['index-en.html', 'index-es.html', 'index-it.html', 'ontology.xml', '.htaccess', 'alo.owl.widoco.conf']
#         # Until the issue is fixed for Widoco
#         #docs_files = ['index-en.html', 'ontology.xml', '.htaccess', 'alo.owl.widoco.conf']
#         for f in docs_files_alo:
#             ff = os.path.join('alo.owl/documentation', f)
#             files_to_check.append(ff)
#         for f in docs_files_geo:
#             ff = os.path.join('geolinkeddata.owl/documentation/doc', f)
#             files_to_check.append(ff)
#         for f in ['.htaccess', 'geolinkeddata.owl.widoco.conf']:
#             ff = os.path.join('geolinkeddata.owl/documentation', f)
#             files_to_check.append(ff)
#         print("---------------\n\n\n\n\n----- IN THE MIDDLE -----test_doc_multi_lang###############\n\n")
#         for f in files_to_check:
#             fdir_to_check = os.path.join(resources_dir, f)
#             print(fdir_to_check)
#             self.assertTrue(os.path.exists(fdir_to_check), msg=(f+" does not exists"))
#         delete_all_repos_from_db()
#         # p.terminate()
#         print("------------------\n\n\n\n\n-------------------test_doc_multi_lang###############\n\n")
#
