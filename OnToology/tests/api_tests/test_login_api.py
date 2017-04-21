
import string
import random

from unittest import TestCase
#from mongoengine.django.tests import MongoTestCase as TestCase
from  OnToology.models import OUser, Repo


class TestLoginAPIs(TestCase):
    def setUp(self):
        sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
        user = OUser()
        user.email = "test@test.com"
        user.username = user.email
        user.password = sec
        user.token = sec
        user.save()

    def test_login(self):
        print 'passing test_login'
        #self.assertEqual(self, "a", "a", "a does not equal b")

