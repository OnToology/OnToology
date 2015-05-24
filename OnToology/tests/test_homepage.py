from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner
import os


 
#Testing the home page
class HomePageInitTestCase123(TestCase):
            
    def test_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, 'error in status_code of the homepage init test')
 
    def _fixture_setup(self):
        return
 
    def _fixture_teardown(self):
        return

