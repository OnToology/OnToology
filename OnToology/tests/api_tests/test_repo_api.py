import json
import string
import random

import os
from . import create_user

from django.test import Client
from unittest import TestCase
from OnToology.models import *


HTTP_AUTHORIZATION

class TestRepoAPI(TestCase):
    def setUp(self):
        if len(OUser.objects.all()) == 0:
            create_user()

    def test_add_repo(self):
        user = OUser.objects.all()[0]
        c = Client()
        url = StringField(max_length=200, default='Not set yet')
        last_used = DateTimeField(default=datetime.now())
        state = StringField(max_length=300, default='Ready')
        owner = StringField(max_length=100, default='no')
        previsual = BooleanField(default=False)
        previsual_page_available = BooleanField(default=False)
        notes = StringField(default='')

        response = c.post('/api/repos', {'url': self.url, 'owner': user.username},
                          HTTP_AUTHORIZATION='Token '+user.token)
        self.assertEqual(response.status_code, 201, msg='repo is not created')
        jresponse = json.loads(response.content)
        self.assertIn('token', jresponse, msg='token is not returned')
        self.assertEqual(jresponse['token'], self.token)


