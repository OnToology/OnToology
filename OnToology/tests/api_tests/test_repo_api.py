import json
import string
import random

import os
from . import create_user

from django.test import Client
from unittest import TestCase
from OnToology.models import *


class TestRepoAPI(TestCase):
    def setUp(self):
        if len(OUser.objects.all()) == 0:
            create_user()
        self.url = 'ahmad88me/demo'
        self.owner = StringField(max_length=100, default='no')
        self.user = OUser.objects.all()[0]

    def test_add_repo(self):
        c = Client()
        response = c.post('/api/repos', {'url': self.url, 'owner': self.user.username},
                          HTTP_AUTHORIZATION='Token '+self.user.token)
        self.assertEqual(response.status_code, 201,
                         msg='repo is not created, status_code: '+str(response.status_code)+response.content)
        jresponse = json.loads(response.content)

    def test_list_repos(self):
        c = Client()
        response = c.get('/api/repos', HTTP_AUTHORIZATION='Token '+self.user.token)
        self.assertEqual(response.status_code, 200, msg=response.content)
        jresponse = json.loads(response.content)
        self.assertIn('repos', jresponse, msg='repos is not in the response')
        self.assertEqual(jresponse['repos'][0], Repo.objects.all()[0].json())


