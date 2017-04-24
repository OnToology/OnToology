import json
import string
import random

import os
from . import create_user, delete_all_repos, create_repo, delete_all_publishnames, create_publishname

from django.test import Client
from unittest import TestCase
from OnToology.models import *


class TestPublishAPI(TestCase):
    def setUp(self):
        if len(OUser.objects.all()) == 0:
            create_user()
        self.url = 'ahmad88me/demo'
        self.user = OUser.objects.all()[0]
        delete_all_repos()
        create_repo(url=self.url, user=self.user)

    def test_add_publishname(self):
        delete_all_publishnames()
        c = Client()
        response = c.post('/api/publishnames', {'name': 'myalo', 'repo': 'ahmad88me/demo', 'ontology': '/alo.owl'},
                          HTTP_AUTHORIZATION='Token ' + self.user.token)
        self.assertEqual(response.status_code, 200, msg='status code is not 200> '+response.content)
        self.assertEqual(len(PublishName.objects.all()), 1, msg='PublishName is not added')
