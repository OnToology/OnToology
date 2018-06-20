import pkgutil
import unittest

from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner

from OnToology import settings
from OnToology.models import *


from mongoengine import connection, connect
import pyclbr

def suite():
    return unittest.TestLoader().discover("OnToology.tests", pattern="test*.py")


class NoSQLTestRunner(DjangoTestSuiteRunner):
    def setup_databases(self):
        settings.test_conf['local'] = True
        settings.test_conf['fork'] = True
        settings.test_conf['clone'] = True
        settings.test_conf['push'] = True
        settings.test_conf['pull'] = True

        self.clearing_db_connection()
        new_db_name = "test_OnToology"
        connect(new_db_name)

    def teardown_databases(self, *args):
        db_name = connection._connection_settings['default']['name']
        connection.get_connection().drop_database(db_name)
        connection.disconnect()

    @classmethod
    def clearing_db_connection(cls):
        """
        Only used by me
        :return:
        """
        # disconnect the connection with the db
        connection.disconnect()
        # remove the connection details
        connection._dbs = {}
        connection._connections = {}
        connection._connection_settings = {}
        # getting call classes defined in models.py
        models = pyclbr.readmodule("OnToology.models").keys()
        for class_model in models:
            # delete the collection to prevent automatically connecting with the old db (the live one)
            del globals()[class_model]._collection


class NoSQLTestCase(TestCase):

    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass






