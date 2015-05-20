from django.test import TestCase
import os
from github import Github
 
 
import unittest
from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner
import os
from github import Github
from subprocess import call
import time
from OnToology import autoncore, views
 
from OnToology.tests import  mimic_webhook
 
 
class LocalRepoTestCase(TestCase):
    def setUp(self):   
    #def __init__(self):
        self.test_repo = os.environ['test_repo']
        self.test_ont_hl = os.environ['test_ont_hl']
        self.test_ont_nl = os.environ['test_ont_nl']
        self.test_folder = os.environ['test_folder']
        self.test_ont_hl_abs = os.path.join(self.test_folder,self.test_ont_hl)
        self.test_ont_nl_abs = os.path.join(self.test_folder,self.test_ont_nl)
        self.username = os.environ['user_github_username']
        self.password = os.environ['user_github_password']
        self.g = Github(self.username,self.password)
        self.collaborator=autoncore.ToolUser
        self.notification_url='http://127.0.0.1:8000/'
         
         
    def pushChanges(self):# I need to verify if the commands is executed successfully
        gu = "git config  user.email \"%s\";" %(self.username)
        gu+= "git config  user.name \"%s\" ;" %(self.username.split('@')[0])
        comm =  "cd "+self.test_folder+";"+gu+" git add . "    
        print comm
        call(comm,shell=True)
        comm = "cd "+self.test_folder+";"+gu+" git commit -m 'automation test' "
        print comm
        call(comm,shell=True)
        gup = "git config push.default matching;"
        comm =  "cd "+self.test_folder+";"+gu+gup+" git push "
        print comm
        call(comm,shell=True)
        time.sleep(15)
      
 
    def getRepo(self):
        return self.g.get_repo(self.test_repo)
         
     
    def addWebhook(self):
        self.removeWebhook()
        res = autoncore.add_webhook(self.test_repo,self.notification_url,self.g)
        if 'error' not in res:
            res['error'] ='just for now'
        self.assertTrue(res['status'],res['error'])
         
         
    def removeWebhook(self):
        #res = True
        for hook in self.getRepo().get_hooks():
            print 'hook_url: '+hook.url
            if self.notification_url in hook.config['url']:
                print 'will delete: '+hook.config['url']
                hook.delete()
            else:
                print 'not match: '+hook.config['url']   
                #res = True
                #break
        #self.assertTrue(res,'Webhook does not exists')    
         
     
    def addCollaborator(self):
        g_auth_user = self.g.get_user()# this to get authenticated if login is not passed
        # and add collaborator expects NamedUser
        res = autoncore.add_collaborator(self.test_repo,self.g.get_user(g_auth_user.login),self.g)
        if 'error' not in res:
            res['error'] = 'this error should not be showen'
        self.assertTrue(res['status'], res['error'])
         
     
    def removeCollaborator(self):
        self.getRepo().remove_from_collaborators(self.collaborator)
         
         
    def updateOntologies(self):
        text_flag = '<!--Automated test1-->'
        text_alternative_flag='<!--Automated test2-->'
        with open(self.test_ont_hl_abs,'w+') as f:
            for line in f:
                if text_flag in line:
                    f.seek(-len(text_flag),os.SEEK_END)
                    f.write(text_alternative_flag)
                    break
                elif text_alternative_flag in line:
                    f.seek(-len(text_alternative_flag),os.SEEK_END)
                    f.write(text_flag)
                    break
                 
        with open(self.test_ont_nl_abs,'w+') as f:
            for line in f:
                if text_flag in line:
                    f.seek(-len(text_flag),os.SEEK_END)
                    f.write(text_alternative_flag)
                    break
                elif text_alternative_flag in line:
                    f.seek(-len(text_alternative_flag),os.SEEK_END)
                    f.write(text_flag)
                    break
         
      
         
    def _fixture_setup(self):
        return
 
    def _fixture_teardown(self):
        return
