import json
import string
import random

import os
from .api_util import create_user, delete_all_repos_from_db, create_repo

from django.test import Client
from unittest import TestCase
from OnToology.models import *
from .serializer import Serializer


class TestRepoAPI(Serializer, TestCase):
    def setUp(self):
        if len(OUser.objects.all()) == 0:
            create_user()
        self.url = 'ahmad88me/ontoology-auto-test-no-res'
        self.user = OUser.objects.all()[0]

    def test_add_repo(self):
        delete_all_repos_from_db()
        c = Client()
        response = c.post('/api/repos', {'url': self.url, 'owner': self.user.username},
                          HTTP_AUTHORIZATION='Token '+self.user.token)
        self.assertEqual(response.status_code, 201,
                         msg='repo is not created, status_code: '+str(response.status_code)+str(response.content))
        self.assertGreaterEqual(len(Repo.objects.all()), 1, msg='repo is not added')

    def test_add_repo_missing_parameters(self):
        c = Client()
        response = c.post('/api/repos',
                          HTTP_AUTHORIZATION='Token '+self.user.token)
        self.assertEqual(response.status_code, 400)

    def test_add_repo_authorization(self):
        c = Client()
        response = c.post('/api/repos', {'url': self.url, 'owner': self.user.username},
                          HTTP_AUTHORIZATION='Token ' + self.user.token+"wrong")
        self.assertEqual(response.status_code, 401)

    def test_list_repos(self):
        delete_all_repos_from_db()
        create_repo(url=self.url)
        c = Client()
        response = c.get('/api/repos', HTTP_AUTHORIZATION='Token '+self.user.token)
        self.assertEqual(response.status_code, 200, msg=response.content)
        jresponse = json.loads(response.content)
        self.assertIn('repos', jresponse, msg='repos is not in the response')
        self.assertEqual(jresponse['repos'][0], Repo.objects.all()[0].json())

    def test_delete_repo(self):
        delete_all_repos_from_db()
        create_repo(url=self.url)
        repoid = str(Repo.objects.all()[0].id)
        c = Client()
        response = c.delete('/api/repos/'+repoid, HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 204, msg=str(response.content))
        self.assertEqual(len(Repo.objects.all()), 0, msg="the repo is not deleted")

    def test_add_collaborator(self):
        delete_all_repos_from_db()
        create_repo(url=self.url)
        from OnToology.autoncore import add_collaborator, init_g
        g = init_g()
        j = add_collaborator(target_repo=self.url, user=self.url.split('/')[0], newg=g)
        print(j)
        self.assertTrue(j['status'], msg="Error adding the collaborator")