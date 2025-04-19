import unittest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.http import HttpResponseRedirect
from OnToology.views import home_view

# Shared environment variables for all tests
ENV_PATCH = {
    'wget_dir': '/tmp/wget',
    'client_id_public': 'public_id',
    'client_secret_public': 'public_secret',
    'client_id_private': 'private_id',
    'client_secret_private': 'private_secret',
    'client_id_login': 'login_id',
    'client_secret_login': 'login_secret',
    'SECRET_KEY': 'secret',
    'publish_dir': '/tmp/publish'
}


class HomeViewTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = MagicMock()
        self.user.email = 'test@example.com'

    def _get_context(self, mock_render):
        args, _ = mock_render.call_args
        return args[2] if len(args) > 2 else {}

    @patch('OnToology.views.render')
    @patch('OnToology.views.get_managers', return_value=['test@example.com'])
    @patch('OnToology.views.read_stats', return_value={})
    @patch('OnToology.views.Repo.objects.order_by')
    @patch('OnToology.views.OUser.objects.all')
    def test_home_view_without_target_repo(self, mock_users_all, mock_repo_order, mock_stats, mock_get_managers, mock_render):
        request = self.factory.get('/')
        request.user = self.user

        mock_repo_order.return_value = MagicMock()
        mock_users_all.return_value = ['user1', 'user2']

        response = home_view(request)
        context = self._get_context(mock_render)

        self.assertIn('repos', context)
        self.assertIn('num_of_users', context)
        self.assertIn('num_of_repos', context)
        self.assertIn('stats', context)

    @patch('OnToology.views.get_repo_name_from_url', return_value=None)
    @patch('OnToology.views.render')
    def test_home_view_invalid_target_repo(self, mock_render, mock_get_repo_name):
        request = self.factory.get('/', {'target_repo': 'invalid/repo/url'})
        request.user = self.user

        home_view(request)

        mock_render.assert_called_once_with(request, 'msg.html', {'msg': 'please enter a valid repo'})

    @patch.dict('OnToology.views.os.environ', ENV_PATCH, clear=True)
    @patch('OnToology.views.call', return_value=0)
    @patch('OnToology.views.get_repo_name_from_url', return_value='owner/repo')
    @patch('OnToology.views.init_g')
    @patch('OnToology.views.webhook_access', return_value=('http://github.com/redirect', 'randomstate'))
    def test_home_view_valid_public_repo(self, mock_webhook_access, mock_init_g, mock_get_repo_name, mock_call):
        request = self.factory.get('/', {'target_repo': 'http://github.com/owner/repo'})
        request.user = self.user
        request.session = {}

        response = home_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, 'http://github.com/redirect')
        self.assertEqual(request.session['target_repo'], 'owner/repo')
        self.assertEqual(request.session['state'], 'randomstate')
        self.assertEqual(request.session['access_token_time'], '1')

    @patch.dict('OnToology.views.os.environ', ENV_PATCH, clear=True)
    @patch('OnToology.views.call', return_value=1)
    @patch('OnToology.views.get_repo_name_from_url', return_value='owner/repo')
    @patch('OnToology.views.init_g')
    @patch('OnToology.views.render')
    def test_home_view_private_repo(self, mock_render, mock_init_g, mock_get_repo_name, mock_call):
        request = self.factory.get('/', {'target_repo': 'http://github.com/owner/repo'})
        request.user = self.user

        home_view(request)
        context = self._get_context(mock_render)

        self.assertIn('Private repos are not currently supported', context['msg'])

    @patch('OnToology.views.get_managers', side_effect=Exception("Failed"))
    @patch('OnToology.views.read_stats', return_value={})
    @patch('OnToology.views.render')
    @patch('OnToology.views.Repo.objects.order_by')
    @patch('OnToology.views.OUser.objects.all')
    def test_home_view_get_managers_exception(self, mock_users_all, mock_repo_order, mock_render, mock_stats, mock_get_managers):
        request = self.factory.get('/')
        request.user = self.user

        mock_repo_order.return_value = MagicMock()
        mock_users_all.return_value = ['user1', 'user2']

        home_view(request)
        context = self._get_context(mock_render)

        self.assertFalse(context['manager'])  # manager should be False on exception


if __name__ == '__main__':
    unittest.main()
