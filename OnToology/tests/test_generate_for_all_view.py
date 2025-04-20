import json
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from unittest.mock import patch, MagicMock
from OnToology.views import generateforall_view
from OnToology.models import OUser, Repo


class GenerateForAllViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_email = 'user@example.com'
        self.repo_url = 'http://github.com/user/repo'
        self.branch = 'main'
        self.ouser = OUser.objects.create_user(username='user1', email=self.user_email, password='pass')
        self.repo = Repo.objects.create(url=self.repo_url)

    def create_request(self, repo=None, branch=None):
        data = {}
        if repo is not None:
            data['repo'] = repo
        if branch is not None:
            data['branch'] = branch
        request = self.factory.get('/generateforall', data)
        request.user = self.ouser
        # request.user.is_authenticated = True
        return request

    def test_missing_repo_redirects(self):
        request = self.create_request(branch=self.branch)
        response = generateforall_view(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.status_code, 302)

    @patch('OnToology.views.render')
    def test_missing_branch_returns_error(self, mock_render):
        request = self.create_request(repo=self.repo_url)
        response = generateforall_view(request)
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        self.assertIn('A branch is expected', args[2]['msg'])

    @patch('OnToology.views.render')
    def test_user_without_repo_access(self, mock_render):
        request = self.create_request(repo=self.repo_url, branch=self.branch)
        # Ensure user has no access by not linking the repo to ouser
        generateforall_view(request)
        args, kwargs = mock_render.call_args
        self.assertIn('You need to register', args[2]['msg'])

    @patch('OnToology.views.generateforall', return_value={'status': True})
    @patch('OnToology.views.render')
    def test_generate_successful(self, mock_render, mock_generate):
        self.ouser.repos.add(self.repo)
        request = self.create_request(repo=self.repo_url, branch=self.branch)
        generateforall_view(request)
        args, kwargs = mock_render.call_args
        self.assertIn('Soon', args[2]['msg'])

    @patch('OnToology.views.generateforall', return_value={'status': False, 'error': 'Some error'})
    @patch('OnToology.views.render')
    def test_generate_failure(self, mock_render, mock_generate):
        self.ouser.repos.add(self.repo)
        request = self.create_request(repo=self.repo_url, branch=self.branch)
        generateforall_view(request)
        args, kwargs = mock_render.call_args
        self.assertIn('Some error', args[2]['msg'])

    @patch('OnToology.views.generateforall', side_effect=Exception('internal error'))
    @patch('OnToology.views.render')
    def test_generate_exception(self, mock_render, mock_generate):
        self.ouser.repos.add(self.repo)
        request = self.create_request(repo=self.repo_url, branch=self.branch)
        generateforall_view(request)
        args, kwargs = mock_render.call_args
        self.assertIn('Internal error', args[2]['msg'])
