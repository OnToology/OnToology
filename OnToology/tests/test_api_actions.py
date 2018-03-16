import json
import string
import random

import os
from subprocess import call
from api_util import create_user, create_repo, delete_all_repos_from_db, get_repo_resource_dir

from django.test import Client
from unittest import TestCase
from OnToology.models import OUser, Repo


class TestActionAPIs(TestCase):
    def setUp(self):
        if len(OUser.objects.all()) == 0:
            create_user()
        self.url = 'ahmad88me/demo'
        self.user = OUser.objects.all()[0]

    # as widoco create a doc for the the ones with hash e.g. myurl#abc
    # def test_generate_all_check_generated_resources_slash(self):
    #     import OnToology.settings as settings
    #     resources_dir = get_repo_resource_dir(os.environ['test_user_email'])
    #     # The below two assertion is to protect the deletion of important files
    #     self.assertEqual(resources_dir.split('/')[-1], 'OnToology', msg='might be a wrong resources dir OnToology')
    #     self.assertIn(os.environ['test_user_email'], resources_dir, msg='might be a wrong resources dir or wrong user')
    #     # print "will delete %s" % resources_dir
    #     # comm = "rm -Rf %s" % resources_dir
    #     # print comm
    #     settings.test_conf['local'] = True
    #     settings.test_conf['fork'] = False
    #     settings.test_conf['clone'] = False
    #     settings.test_conf['push'] = False
    #     settings.test_conf['pull'] = False
    #     delete_all_repos_from_db()
    #     create_repo()
    #     c = Client()
    #     response = c.post('/api/generate_all', {'url': Repo.objects.all()[0].url},
    #                       HTTP_AUTHORIZATION='Token '+self.user.token)
    #     self.assertEqual(response.status_code, 202, msg=response.content)
    #
    #     files_to_check = ['alo.owl/OnToology.cfg',]
    #     docs_files = ['index-en.html', 'ontology.xml', '.htaccess', 'alo.owl.widoco.conf']
    #     diagrams_files = ['ar2dtool-class/alo.owl.png', 'ar2dtool-taxonomy/alo.owl.png']
    #     eval_files = ['oops.html']
    #     for f in docs_files:
    #         ff = os.path.join('alo.owl/documentation', f)
    #         files_to_check.append(ff)
    #     for f in diagrams_files:
    #         ff = os.path.join('alo.owl/diagrams', f)
    #         files_to_check.append(ff)
    #     for f in eval_files:
    #         ff = os.path.join('alo.owl/evaluation', f)
    #         files_to_check.append(ff)
    #     for f in files_to_check:
    #         print os.path.join(resources_dir, f)
    #         self.assertTrue(os.path.exists(os.path.join(resources_dir, f)), msg=(f+" does not exists"))
    #     delete_all_repos_from_db()

    def test_generate_all_check_generated_resources_hash(self):
        import OnToology.settings as settings
        resources_dir = get_repo_resource_dir(os.environ['test_user_email'])
        # The below two assertion is to protect the deletion of important files
        self.assertEqual(resources_dir.split('/')[-1], 'OnToology', msg='might be a wrong resources dir OnToology')
        self.assertIn(os.environ['test_user_email'], resources_dir,
                      msg='might be a wrong resources dir or wrong user')
        # print "will delete %s" % resources_dir
        # comm = "rm -Rf %s" % resources_dir
        # print comm
        settings.test_conf['local'] = True
        settings.test_conf['fork'] = False
        settings.test_conf['clone'] = False
        settings.test_conf['push'] = False
        settings.test_conf['pull'] = False
        delete_all_repos_from_db()
        create_repo()
        c = Client()
        response = c.post('/api/generate_all', {'url': Repo.objects.all()[0].url},
                          HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 202, msg=response.content)

        files_to_check = ['geolinkeddata.owl/OnToology.cfg', ]
        docs_files = ['doc/index-en.html', 'doc/ontology.xml', '.htaccess', 'geolinkeddata.owl.widoco.conf']
        diagrams_files = ['ar2dtool-class/geolinkeddata.owl.png', 'ar2dtool-taxonomy/geolinkeddata.owl.png']
        eval_files = ['oops.html']
        for f in docs_files:
            ff = os.path.join('geolinkeddata.owl/documentation', f)
            files_to_check.append(ff)
        for f in diagrams_files:
            ff = os.path.join('geolinkeddata.owl/diagrams', f)
            files_to_check.append(ff)
        # Because oops APIs at the moment gives an error for this ontology
        for f in eval_files:
            ff = os.path.join('geolinkeddata.owl/evaluation', f)
            files_to_check.append(ff)
        for f in files_to_check:
            print os.path.join(resources_dir, f)
            self.assertTrue(os.path.exists(os.path.join(resources_dir, f)), msg=(f + " does not exists"))
        delete_all_repos_from_db()

# # Included by the previous two cases
#     # def test_generate_all_check_status(self):
#     #     create_repo()
#     #     c = Client()
#     #     response = c.post('/api/generate_all', {'url': Repo.objects.all()[0].url},
#     #                       HTTP_AUTHORIZATION='Token '+self.user.token)
#     #     self.assertEqual(response.status_code, 202, msg=response.content)
#     #     print get_repo_resource_dir(os.environ['test_user_email'])
#     #     delete_all_repos_from_db()
#
#     def test_generate_all_wrong_repo(self):
#         create_repo()
#         c = Client()
#         response = c.post('/api/generate_all', {'url': Repo.objects.all()[0].url+'wrong'},
#                           HTTP_AUTHORIZATION='Token '+self.user.token)
#         self.assertEqual(response.status_code, 404, msg=response.content)
#         delete_all_repos_from_db()
#
#     def test_generate_all_missing_parameter(self):
#         create_repo()
#         c = Client()
#         response = c.post('/api/generate_all', HTTP_AUTHORIZATION='Token '+self.user.token)
#         self.assertEqual(response.status_code, 400, msg=response.content)
#         delete_all_repos_from_db()
#
#     def test_generate_all_missing_authorization(self):
#         create_repo()
#         c = Client()
#         response = c.post('/api/generate_all', {'url': Repo.objects.all()[0].url})
#         self.assertEqual(response.status_code, 401, msg=response.content)
#         delete_all_repos_from_db()
