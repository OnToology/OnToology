# import json
# import string
# import random
#
# import os
# from api_util import create_user, delete_all_repos_from_db, create_repo, delete_all_publishnames, create_publishname
#
# from django.test import Client
# from unittest import TestCase
# from OnToology.models import *
#
#
# class TestPublishAPI(TestCase):
#     def setUp(self):
#         # if len(OUser.objects.all()) == 0:
#         #     create_user()
#         OUser.objects.delete()
#         create_user()
#         self.url_no_res = 'ahmad88me/ontoology-auto-test-no-res'
#         self.url_with_res = 'ahmad88me/ontoology-auto-test-with-res'
#         self.user = OUser.objects.all()[0]
#         print "will delete from all"
#         delete_all_repos_from_db()
#         print "test publish API"
#         create_repo(url=self.url_no_res, user=self.user)
#         create_repo(url=self.url_with_res, user=self.user)
#
#     def test_add_publishname_no_doc(self):
#         delete_all_publishnames()
#         c = Client()
#         response = c.post('/api/publishnames', {'name': 'myalo', 'repo': self.url_no_res, 'ontology': '/alo.owl'},
#                           HTTP_AUTHORIZATION='Token ' + self.user.token)
#         print "repos no doc of user"
#         print self.user.repos
#         self.assertEqual(response.status_code, 400, msg='status code is not 400> '+response.content)
#         self.assertEqual(len(PublishName.objects.all()), 0, msg='It should not be added')
#
#     def test_add_publishname_with_doc(self):
#         delete_all_publishnames()
#         c = Client()
#         print "repos of user with doc"
#         print self.user.repos
#         response = c.post('/api/publishnames', {'name': 'myaloautotest', 'repo': self.url_with_res, 'ontology': '/alo.owl'},
#                           HTTP_AUTHORIZATION='Token ' + self.user.token)
#         self.assertEqual(response.status_code, 200, msg='status code is not 200> '+response.content)
#         self.assertEqual(len(PublishName.objects.all()), 1, msg='PublishName is not added')
#
#     # def test_list_publishname(self):
#     #     delete_all_publishnames()
#     #     create_publishname(name='myalo', user=self.user, repo=Repo.objects.all()[0], ontology='/alo.owl')
#     #     c = Client()
#     #     response = c.get('/api/publishnames', HTTP_AUTHORIZATION='Token ' + self.user.token)
#     #     self.assertEqual(response.status_code, 200, msg='status code is not 200> '+response.content)
#     #     jresponse = json.loads(response.content)
#     #     self.assertEqual(len(jresponse['publishnames']), 1, msg='list does not return')