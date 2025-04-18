import unittest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from OnToology.views import get_ontologies
import json


class GetOntologiesTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = MagicMock()
        self.user.is_authenticated = True
        self.repo_url = 'http://github.com/user/repo'
        self.branch = 'main'

    def test_missing_branch_or_repo(self):
        request = self.factory.get('/get_ontologies?branch=main')  # missing repo
        request.user = self.user

        response = get_ontologies(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('expecting the branch and repo', response.content.decode())

    def test_repo_not_belonging_to_user(self):
        request = self.factory.get(f'/get_ontologies?branch={self.branch}&repo={self.repo_url}')
        request.user = self.user
        self.user.repos.filter.return_value = []

        response = get_ontologies(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('This repo does not belong to your user account', response.content.decode())

    @patch('OnToology.views.parse_online_repo_for_ontologies', return_value=['onto1.owl', 'onto2.ttl'])
    @patch('OnToology.views.add_themis_results')
    def test_successful_ontology_extraction(self, mock_add_themis, mock_parse):
        request = self.factory.get(f'/get_ontologies?branch={self.branch}&repo={self.repo_url}')
        request.user = self.user
        self.user.repos.filter.return_value = [MagicMock()]  # Simulate user owning the repo

        response = get_ontologies(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'ontologies': ['onto1.owl', 'onto2.ttl']})

    @patch('OnToology.views.parse_online_repo_for_ontologies', side_effect=Exception('Boom!'))
    @patch('OnToology.views.add_themis_results')
    def test_parsing_exception(self, mock_add_themis, mock_parse):
        request = self.factory.get(f'/get_ontologies?branch={self.branch}&repo={self.repo_url}')
        request.user = self.user
        self.user.repos.filter.return_value = [MagicMock()]

        response = get_ontologies(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Make sure you have the branch and the repository URL are correct', response.content.decode())


if __name__ == '__main__':
    unittest.main()
