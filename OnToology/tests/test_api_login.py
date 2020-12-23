import json
import string
import random

import os

from django.test import Client
from unittest import TestCase
# from mongoengine.django.tests import MongoTestCase as TestCase
from OnToology.models import OUser, Repo
from django.utils import timezone


# class TestLoginAPIs(TestCase):
#     def setUp(self):
#
#         if len(OUser.objects.all()) > 0:
#             OUser.objects.all().delete()
#
#         sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
#         user = OUser()
#         user.email = os.environ['test_user_email']
#         user.username = user.email
#         user.password = os.environ['test_user_token']
#         user.token = sec
#         user.save()
#         self.username = user.username
#         self.password = os.environ['test_user_token']
#         self.token = sec
#
#     def test_login(self):
#         c = Client()
#         response = c.post('/api/login', {'username': self.username, 'password': self.password})
#         self.assertEqual(response.status_code, 200, msg='Error http status code')
#         jresponse = json.loads(response.content)
#         self.assertIn('token', jresponse, msg='token is not returned')
#         self.assertEqual(jresponse['token'], self.token)
#
#     # def test_false(self):
#     #     self.assertTrue(False)
