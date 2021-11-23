import json
import string
import random

import os
from .api_util import create_user, delete_all_repos_from_db, create_repo, delete_all_publishnames
from .api_util import create_publishname, delete_all_users

from django.test import Client
from unittest import TestCase
from OnToology.models import *
from .serializer import Serializer


class TestPublishAPI(Serializer, TestCase):
    def setUp(self):
        delete_all_users()
        if len(OUser.objects.all()) == 0:
            create_user()
        else:
            print("Not all users where deleted")
            raise Exception("Error deleteing users")
        self.url = 'ahmad88me/ontoology-auto-test-no-res'
        self.user = OUser.objects.all()[0]
        self.branch = 'master'
        self.url_no_res = 'ahmad88me/ontoology-auto-test-no-res'
        self.url_with_res = 'ahmad88me/ontoology-auto-test-with-res'
        self.user = OUser.objects.all()[0]
        delete_all_repos_from_db()
        create_repo(url=self.url_no_res, user=self.user)
        create_repo(url=self.url_with_res, user=self.user)
        self.name = 'myalotest'
        self.ontology = '/alo.owl'

    def test_add_publishname_no_doc(self):
        delete_all_publishnames()
        c = Client()
        response = c.post('/api/publishnames', {'name': self.name, 'repo': self.url_no_res, 'ontology': self.ontology, 'branch': self.branch},
                          HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 400, msg='status code is not 400> '+str(response.content))
        self.assertEqual(len(PublishName.objects.all()), 0, msg='It should not be added')

    def test_delete_publishname_existing(self):
        delete_all_publishnames()
        create_publishname(name=self.name, user=self.user, repo=Repo.objects.get(url=self.url_no_res), ontology=self.ontology)
        c = Client()
        response = c.delete('/api/publishnames?name=%s&repo=%s&ontology=%s' % (self.name, self.url_no_res,self.ontology),
                          HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 200, msg='status code is not 200: '+str(response.content))
        self.assertEqual(len(PublishName.objects.all()), 0, msg='It should be deleted')

    def test_delete_publishname_invalid_no_others(self):
        delete_all_publishnames()
        c = Client()
        response = c.delete('/api/publishnames?name=%s&repo=%s&ontology=%s' % (self.name, self.url_no_res,self.ontology),
                          HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 400, msg='status code is not 400: '+str(response.content))
        self.assertEqual(len(PublishName.objects.all()), 0, msg='There should be no publishnames')

    def test_delete_publishname_invalid_with_unrelated_ontology(self):
        delete_all_publishnames()
        invalid_ontology = self.ontology+"a"
        invalid_name = self.name+"a"
        c = Client()
        create_publishname(name=invalid_name, user=self.user, repo=Repo.objects.get(url=self.url_no_res), ontology=invalid_ontology)
        response = c.delete('/api/publishnames?name=%s&repo=%s&ontology=%s' % (self.name, self.url_no_res, self.ontology),
                          HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 400, msg='status code is not 400: '+str(response.content))
        self.assertEqual(len(PublishName.objects.all()), 1, msg='There should be one unrelated publishedname')

    def test_add_publishname_with_doc(self):
        delete_all_publishnames()
        # create_publishname(name=self.name+"-new", user=self.user, repo=Repo.objects.get(url=self.url_no_res), ontology=self.ontology+"new")
        c = Client()
        response = c.post('/api/publishnames', {'name': self.name, 'repo': self.url_with_res, 'ontology': self.ontology, 'branch': self.branch},
                          HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 200, msg='status code is not 200> '+str(response.content))
        self.assertEqual(len(PublishName.objects.all()), 1, msg='PublishName is not added')

    def test_add_publishname_with_doc_reserved_ontology(self):
        delete_all_publishnames()
        create_publishname(name=self.name+"-new", user=self.user, repo=Repo.objects.get(url=self.url_with_res), ontology=self.ontology)
        c = Client()
        response = c.post('/api/publishnames', {'name': self.name+"a", 'repo': self.url_with_res, 'ontology': self.ontology, 'branch': self.branch},
                          HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 400, msg='status code is not 400> '+str(response.content))
        self.assertEqual(len(PublishName.objects.all()), 1, msg='PublishName is not added')

    def test_add_publishname_with_doc_republish(self):
        delete_all_publishnames()
        create_publishname(name=self.name, user=self.user, repo=Repo.objects.get(url=self.url_with_res), ontology=self.ontology)
        c = Client()
        response = c.post('/api/publishnames', {'name': "", 'repo': self.url_with_res, 'ontology': self.ontology, 'branch': self.branch},
                          HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 200, msg='status code is not 200> '+str(response.content))
        self.assertEqual(len(PublishName.objects.all()), 1, msg='PublishName is not added')

    def test_list_publishname(self):
        delete_all_publishnames()
        create_publishname(name=self.name, user=self.user, repo=Repo.objects.get(url=self.url_no_res), ontology=self.ontology)
        c = Client()
        response = c.get('/api/publishnames', HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 200, msg='status code is not 200> '+str(response.content))
        jresponse = response.json()
        self.assertEqual(len(jresponse['publishnames']), 1, msg='list does not return')

