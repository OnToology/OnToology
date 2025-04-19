from django.test import TestCase, RequestFactory
from django.http import HttpResponseRedirect
from unittest.mock import patch, MagicMock
from OnToology.models import OUser
from OnToology.views import get_access_token
from django.http import HttpResponse


class GetAccessTokenTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = OUser.objects.create(username='tokenuser', email='token@example.com')

    @patch('OnToology.views.requests.post')
    @patch('OnToology.views.add_coll_and_webhook')
    def test_valid_access_token(self, mock_add_coll_and_webhook, mock_requests_post):
        mock_response = MagicMock()
        mock_response.text = 'access_token=mytoken&scope=repo&token_type=bearer'
        mock_requests_post.return_value = mock_response
        mock_add_coll_and_webhook.return_value = HttpResponseRedirect('/success')

        request = self.factory.get('/get_access_token', {'state': 'xyz', 'code': 'abc'})
        request.user = self.user
        request.session = {'state': 'xyz'}

        response = get_access_token(request)

        self.assertEqual(request.session['access_token'], 'mytoken')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/success')

    def test_invalid_state_redirects_home(self):
        request = self.factory.get('/get_access_token', {'state': 'wrong'})
        request.user = self.user
        request.session = {'state': 'correct'}

        response = get_access_token(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    @patch('OnToology.views.requests.post')
    @patch('OnToology.views.render')
    def test_github_token_parsing_failure(self, mock_render, mock_requests_post):
        mock_response = MagicMock()
        mock_response.text = 'invalid response without equal sign'
        mock_requests_post.return_value = mock_response

        mock_render.return_value = HttpResponse('error', status=200)

        request = self.factory.get('/get_access_token', {'state': 'xyz', 'code': 'abc'})
        request.user = self.user
        request.session = {'state': 'xyz'}

        response = get_access_token(request)

        mock_render.assert_called_once()
        self.assertEqual(response.status_code, 200)

    @patch('OnToology.views.requests.post')
    def test_missing_access_token_redirects_home(self, mock_requests_post):
        mock_response = MagicMock()
        mock_response.text = 'scope=repo&token_type=bearer'  # no access_token
        mock_requests_post.return_value = mock_response

        request = self.factory.get('/get_access_token', {'state': 'xyz', 'code': 'abc'})
        request.user = self.user
        request.session = {'state': 'xyz'}

        response = get_access_token(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
