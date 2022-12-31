from django.test import Client
from unittest import TestCase
from .serializer import Serializer
from OnToology.models import OUser, Repo
from .api_util import create_user, create_repo, delete_all_repos_from_db, get_repo_resource_dir, clone_if_not, delete_all_users
import json


class TestOutline(Serializer, TestCase):
    def setUp(self):
        print("setup TestActionAPIs")
        delete_all_users()
        delete_all_repos_from_db()
        if len(OUser.objects.all()) == 0:
            create_user()
        self.url = 'ahmad88me/ontoology-auto-test-no-res'
        self.user = OUser.objects.all()[0]


    def test_outline_no_status(self):
        delete_all_repos_from_db()
        self.assertEqual(0, len(Repo.objects.all()))
        create_repo(url=self.url, user=self.user)
        self.assertEqual(1, len(Repo.objects.all()))
        c = Client()
        c.force_login(self.user)
        response = c.get('/get_outline',
                          HTTP_AUTHORIZATION='Token  ' +self.user.token, raise_request_exception=True)
        # print('Response status code : ' + str(response.status_code))
        # print('Response content : ' + str(response.content))
        self.assertEqual(response.status_code, 200, msg=response.content)

    def test_outline_with_status(self):
        delete_all_repos_from_db()
        self.assertEqual(0, len(Repo.objects.all()))
        r = create_repo(url=self.url, user=self.user)
        r.update_ontology_status('alo.owl', 'pending')
        r.update_ontology_status('blo.owl', 'finished')
        self.assertEqual(1, len(Repo.objects.all()))
        c = Client()
        c.force_login(self.user)
        response = c.get('/get_outline',
                          HTTP_AUTHORIZATION='Token  ' +self.user.token, raise_request_exception=True)
        # print('Response status code : ' + str(response.status_code))
        # print('Response content : ' + str(response.content))
        self.assertEqual(response.status_code, 200, msg=response.content)
        self.assertEqual(response.json()['stages']['pending'][0], 'alo.owl')
        self.assertEqual(response.json()['stages']['finished'][0], 'blo.owl')
        delete_all_repos_from_db()