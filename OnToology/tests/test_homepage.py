from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner
import os
 
#username = os.environ['OnToology_Test_Username']
#password = os.environ['OnToology_Test_Password']
 
 
# class NoSQLTestRunner(DjangoTestSuiteRunner):
#     def setup_databases(self):
#         pass
#     def teardown_databases(self, *args):
#         pass
# 
# 
# class NoSQLTestCase(TestCase):
#     def _fixture_setup(self):
#         pass
#     def _fixture_teardown(self):
#         pass
 
 
#Testing the home page
class HomePageInitTestCase123(TestCase):
            
    def test_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, 'error in status_code of the homepage init test')
 
    def _fixture_setup(self):
        return
 
    def _fixture_teardown(self):
        return

