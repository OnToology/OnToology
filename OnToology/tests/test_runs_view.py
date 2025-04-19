import unittest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.http import HttpResponseRedirect
from django.urls import reverse
from OnToology.views import runs_view


class RunsViewTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = MagicMock()
        self.user.is_authenticated = True
        self.repo_url = 'http://github.com/user/repo'

    @patch('OnToology.views.render')
    def test_runs_view_no_repo_param(self, mock_render):
        request = self.factory.get('/runs')
        request.user = self.user
        self.user.repos.all.return_value = ['repo1', 'repo2']

        runs_view(request)

        mock_render.assert_called_once_with(request, 'user_repos.html', {'repos': ['repo1', 'repo2']})

    @patch('OnToology.views.render')
    @patch('OnToology.views.Repo.objects.filter', return_value=[])
    def test_runs_view_repo_not_found(self, mock_repo_filter, mock_render):
        request = self.factory.get('/runs?repo=' + self.repo_url)
        request.user = self.user

        response = runs_view(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse('profile'))

    @patch('OnToology.views.render')
    @patch('OnToology.views.Repo.objects.filter')
    def test_runs_view_repo_not_owned_by_user(self, mock_repo_filter, mock_render):
        request = self.factory.get('/runs?repo=' + self.repo_url)
        request.user = self.user
        mock_repo = MagicMock()
        mock_repo_filter.return_value = [mock_repo]
        self.user.repos.all.return_value = []

        runs_view(request)

        mock_render.assert_called_once_with(request, 'msg.html', {
            'msg': 'This repo does not belong to the loggedin user. Try to add it and try again.'
        })

    @patch('OnToology.views.render')
    @patch('OnToology.views.ORun.objects.filter')
    @patch('OnToology.views.Repo.objects.filter')
    def test_runs_view_valid_repo_owned_by_user(self, mock_repo_filter, mock_orun_filter, mock_render):
        request = self.factory.get('/runs?repo=' + self.repo_url)
        request.user = self.user
        mock_repo = MagicMock()
        mock_repo_filter.return_value = [mock_repo]
        self.user.repos.all.return_value = [mock_repo]
        mock_orun_filter.return_value.order_by.return_value = ['run1', 'run2']

        runs_view(request)

        mock_render.assert_called_once_with(request, 'runs.html', {'oruns': ['run1', 'run2']})

    @patch('OnToology.views.reverse', return_value='/profile')
    @patch('OnToology.views.HttpResponseRedirect')
    @patch('OnToology.views.Repo.objects.filter', side_effect=Exception("boom"))
    def test_runs_view_exception_redirects_to_profile(self, mock_repo_filter, mock_http_redirect, mock_reverse):
        request = self.factory.get('/runs?repo=' + self.repo_url)
        request.user = self.user

        runs_view(request)

        mock_http_redirect.assert_called_once_with('/profile')


if __name__ == '__main__':
    unittest.main()
