import unittest

from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner

import OnToology.settings as settings


def suite():
    return unittest.TestLoader().discover("OnToology.tests.api_tests", pattern="*.py")

class NoSQLTestRunner(DjangoTestSuiteRunner):
    def setup_databases(self):
        settings.test_conf['local']=True
        settings.TEST = True
        pass
    def teardown_databases(self, *args):
        pass

class NoSQLTestCase(TestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass