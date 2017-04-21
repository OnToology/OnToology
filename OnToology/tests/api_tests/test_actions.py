import json
import string
import random

import os

from . import create_user, create_repo, delete_all_repos

from django.test import Client
from unittest import TestCase
from OnToology.models import OUser, Repo


class TestActionAPIs(TestCase):
    def setUp(self):
        if len(OUser.objects.all()) == 0:
            create_user()
        self.url = 'ahmad88me/demo'
        self.user = OUser.objects.all()[0]

    def test_generate_all(self):
        create_repo()
        c = Client()
        response = c.post('/api/generate_all', {'url': Repo.objects.all()[0].url},
                          HTTP_AUTHORIZATION='Token '+self.user.token)
        self.assertEqual(response.status_code, 202, msg=response.content)
        delete_all_repos()

    def test_generate_all_wrong_repo(self):
        create_repo()
        c = Client()
        response = c.post('/api/generate_all', {'url': Repo.objects.all()[0].url+'wrong'},
                          HTTP_AUTHORIZATION='Token '+self.user.token)
        self.assertEqual(response.status_code, 404, msg=response.content)
        delete_all_repos()

    def test_generate_all_missing_parameter(self):
        create_repo()
        c = Client()
        response = c.post('/api/generate_all', HTTP_AUTHORIZATION='Token '+self.user.token)
        self.assertEqual(response.status_code, 400, msg=response.content)
        delete_all_repos()

    def test_generate_all_missing_authorization(self):
        create_repo()
        c = Client()
        response = c.post('/api/generate_all', {'url': Repo.objects.all()[0].url})
        self.assertEqual(response.status_code, 401, msg=response.content)
        delete_all_repos()