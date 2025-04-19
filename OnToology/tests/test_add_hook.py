import json
from django.test import TestCase, RequestFactory, override_settings
from django.http import JsonResponse
from unittest.mock import patch, MagicMock
from OnToology.views import add_hook
from OnToology.models import Repo, OUser
from django.utils import timezone
from django.conf import settings
from django.test import override_settings
from django.db.models import Model


@override_settings(test_conf={'local': True})
class AddHookTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.repo_url = 'http://github.com/user/repo'
        self.repo_name = 'user/repo'
        self.user_email = 'user@example.com'
        self.payload_template = {
            "ref": "refs/heads/main",
            "head_commit": {
                "message": "Initial commit",
                "modified": ["file1.owl"]
            },
            "repository": {
                "url": self.repo_url,
                "full_name": self.repo_name,
                "owner": {
                    "email": self.user_email
                }
            }
        }

    @patch('OnToology.views.get_changed_files_from_payload', return_value=['file1.owl'])
    @patch('OnToology.views.send_to_magic', return_value=JsonResponse({'status': True}))
    def test_valid_payload_triggers_magic(self, mock_send_to_magic, mock_get_changed):
        payload = json.dumps(self.payload_template)
        request = self.factory.post('/add_hook', {'payload': payload})
        request.headers = {}

        response = add_hook(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['status'])
        mock_send_to_magic.assert_called_once()

    def test_payload_with_gh_pages_branch(self):
        payload_data = self.payload_template.copy()
        payload_data["ref"] = "refs/heads/gh-pages"
        payload = json.dumps(payload_data)
        request = self.factory.post('/add_hook', {'payload': payload})
        request.headers = {}

        response = add_hook(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('gh-pages', data['msg'])

    def test_payload_missing_ref(self):
        payload_data = self.payload_template.copy()
        del payload_data["ref"]
        payload = json.dumps(payload_data)
        request = self.factory.post('/add_hook', {'payload': payload})
        request.headers = {}

        response = add_hook(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('No ref is found', data['error'])

    @patch.dict('OnToology.views.settings.test_conf', {'local': False})
    @patch('OnToology.views.Repo.objects.get')
    def test_merge_commit_creates_repo(self, mock_repo_get):
        payload_data = self.payload_template.copy()
        payload_data["head_commit"]["message"] = "Merge pull request"
        payload_data["commits"] = [{"modified": ["file1.owl"], "added": []}]
        payload = json.dumps(payload_data)
        request = self.factory.post('/add_hook', {'payload': payload})
        request.headers = {}
        response = add_hook(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        print(f"data: {data}")
        self.assertIn('merge request', data['msg'])

    def test_invalid_payload_returns_error(self):
        request = self.factory.post('/add_hook', {'payload': 'not-a-valid-json'})
        request.headers = {}

        response = add_hook(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['status'])
        self.assertIn('error', data)
