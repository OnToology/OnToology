import unittest
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from django.utils import timezone
from OnToology.views import send_to_magic
import json

class SendToMagicTestCase(unittest.TestCase):
    def setUp(self):
        self.changed_files = ['file1.owl', 'file2.ttl']
        self.target_repo = 'http://github.com/user/repo'
        self.branch = 'main'
        self.user_email = 'user@example.com'

    @patch('OnToology.views.sqclient.send')
    def test_successful_send(self, mock_send):
        response = send_to_magic(self.changed_files, self.target_repo, self.branch, self.user_email)
        data = json.loads(response.content)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'status': True})
        mock_send.assert_called_once()
        payload = mock_send.call_args[0][0]
        self.assertEqual(payload['repo'], self.target_repo)
        self.assertEqual(payload['branch'], self.branch)
        self.assertEqual(payload['useremail'], self.user_email)
        self.assertEqual(payload['changedfiles'], self.changed_files)
        self.assertEqual(payload['action'], 'magic')
        self.assertIn('created', payload)

    @patch('OnToology.views.sqclient.send', side_effect=Exception('execv() arg 2 must contain only strings'))
    def test_send_special_char_error(self, mock_send):
        response = send_to_magic(self.changed_files, self.target_repo, self.branch, self.user_email)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data, {
            'status': False,
            'error': 'make sure that your repository filenames does not have accents or special characters'
        })

    @patch('OnToology.views.sqclient.send', side_effect=Exception('some other error'))
    def test_send_generic_error(self, mock_send):
        response = send_to_magic(self.changed_files, self.target_repo, self.branch, self.user_email)
        data = json.loads(response.content)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {
            'status': False,
            'error': 'generic error, please report the problem to us ontoology@delicias.dia.fi.upm.es'
        })
