from django.test import TestCase, RequestFactory
from unittest.mock import patch
from django.http import HttpResponseRedirect
from OnToology.models import Repo, OUser
from OnToology.views import add_coll_and_webhook


class AddCollAndWebhookTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.repo_url = 'http://github.com/user/repo'
        self.user_email = 'user@example.com'

        # Create real user and repo
        self.user = OUser.objects.create(username='testuser', email=self.user_email)
        self.repo = Repo.objects.create(url=self.repo_url)

    def create_request(self, access_token_time='2'):
        request = self.factory.get('/add_coll_and_webhook')
        request.user = self.user
        request.session = {
            'target_repo': self.repo_url,
            'access_token_time': access_token_time
        }
        return request

    @patch('OnToology.views.webhook_access', return_value=('http://github.com/webhook', 'xyz123'))
    def test_redirect_if_access_token_time_1(self, mock_webhook_access):
        request = self.create_request(access_token_time='1')
        response = add_coll_and_webhook(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, 'http://github.com/webhook')
        self.assertEqual(request.session['state'], 'xyz123')
        self.assertEqual(request.session['access_token_time'], '2')

    @patch('OnToology.views.render')
    @patch.dict('OnToology.views.os.environ', {'skip_add_collaborator': 'true'})
    def test_local_environment_skips_hooks(self, mock_render):
        request = self.create_request()
        add_coll_and_webhook(request)

        mock_render.assert_called_once()
        context = mock_render.call_args[0][2]
        self.assertIn('webhook attached', context['msg'])

    @patch('OnToology.views.add_webhook', return_value={'status': False, 'error': '404 error'})
    @patch('OnToology.views.add_collaborator', return_value={'status': False, 'error': '404 error'})
    @patch('OnToology.views.render')
    @patch.dict('OnToology.views.os.environ', {}, clear=True)
    def test_github_404_error(self, mock_render, mock_add_collab, mock_add_hook):
        request = self.create_request()
        add_coll_and_webhook(request)

        context = mock_render.call_args[0][2]
        self.assertIn("You don't have permission", context['msg'])

    @patch('OnToology.views.add_webhook', return_value={'status': False, 'error': 'Hook already exists on this repository'})
    @patch('OnToology.views.add_collaborator', return_value={'status': True, 'msg': 'added'})
    @patch('OnToology.views.render')
    @patch.dict('OnToology.views.os.environ', {}, clear=True)
    def test_hook_already_exists(self, mock_render, mock_add_collab, mock_add_hook):
        request = self.create_request()
        add_coll_and_webhook(request)

        context = mock_render.call_args[0][2]
        self.assertIn("already watched", context['msg'])

    @patch('OnToology.views.render')
    @patch('OnToology.views.add_collaborator', return_value={'status': True, 'msg': 'added'})
    @patch('OnToology.views.add_webhook', return_value={'status': True})
    @patch.dict('OnToology.views.os.environ', {}, clear=True)
    def test_successful_webhook_and_collaborator(self, mock_add_webhook, mock_add_collaborator, mock_render):
        request = self.create_request()
        # Delete repo to force creation in view
        self.repo.delete()

        add_coll_and_webhook(request)

        context = mock_render.call_args[0][2]
        self.assertIn("webhook attached", context['msg'])
        self.assertTrue(Repo.objects.filter(url=self.repo_url).exists())
        self.assertIn(self.repo_url, [r.url for r in self.user.repos.all()])
