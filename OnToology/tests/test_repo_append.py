
from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner
import os
from . import LocalRepoTestCase



class TestAppendRepo(LocalRepoTestCase):
    def __init__(self):
        LocalRepoTestCase.__init__(self)
        self.test_ont_hl_abs = os.path.join(self.test_repo_abs_dir,self.test_ont_hl)
        self.test_ont_nl_abs = os.path.join(self.test_repo_abs_dir,self.test_ont_nl)
        
    def teno_append(self):
        f = open(self.test_ont_hl_abs,'a')
        f.write('<!--Automated test-->')
        f.close()
        f = open(self.test_ont_nl_abs,'a')
        f.write('<!--Automated test-->')
        f.close()
        #self.push_changes()
        
        
