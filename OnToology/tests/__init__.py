import pkgutil
import unittest

from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner

from OnToology import settings
from OnToology.tests import __path__


def suite():
    return unittest.TestLoader().discover("OnToology.tests.api_tests", pattern="*.py")

# print "__path__ is: %s" % str(__path__)

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    # print ' module_name: '+str(module_name)+', is_pkg: '+str(is_pkg)
    module = loader.find_module(module_name).load_module(module_name)
    # print 'dir module: '+str(dir(module))
    for name in dir(module):
        # print 'name: '+str(name)
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, unittest.case.TestCase):
            # print "obj %s" % str(obj)
            exec ('%s = obj' % obj.__name__)


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