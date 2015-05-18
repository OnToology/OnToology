import unittest
from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner
import os
from github import Github
from subprocess import call
import time


def suite():   
    return unittest.TestLoader().discover("OnToology.tests", pattern="*.py")



class NoSQLTestRunner(DjangoTestSuiteRunner):
    def setup_databases(self):
        pass
    def teardown_databases(self, *args):
        pass


class NoSQLTestCase(TestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass
    





class LocalRepoTestCase(TestCase):
        
    def __init__(self):
        self.test_repo_abs_dir = os.environ['test_repo']
        self.test_ont_hl = os.environ['test_ont_hl']
        self.test_ont_nl = os.environ['test_ont_nl']
        self.username = os.environ['user_github_username']
        self.password = os.environ['user_github_password']
        self.g = Github(self.username,self.password)
        
        
    def push_changes(self):
        gu = "git config  user.email \"%s\";" %(self.username)
        gu+="git config  user.name \"%s\" ;" %(self.username.split('@')[0])
        comm =  "cd "+self.test_repo_abs_dir+";"+gu+" git add . "    
        print comm
        call(comm,shell=True)
        comm = "cd "+self.test_repo_abs_dir+";"+gu+" git commit -m 'automation test' "
        print comm
        call(comm,shell=True)
        gup = "git config push.default matching;"
        comm =  "cd "+self.test_repo_abs_dir+";"+gu+gup+" git push "
        print comm
        call(comm,shell=True)
        time.sleep(50)
 
    
        
    def _fixture_setup(self):
        return

    def _fixture_teardown(self):
        return

