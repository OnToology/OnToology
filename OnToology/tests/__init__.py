import unittest
from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner
import os
from github import Github
from subprocess import call, Popen, PIPE
import time
from OnToology import autoncore, views, settings
from _curses import ERR


#import mimic_webhook



def suite():   
    return unittest.TestLoader().discover("OnToology.tests", pattern="test*.py")






 
import pkgutil
import unittest
from OnToology.tests import __path__
 
#print str(__path__)
#resource http://stackoverflow.com/questions/6248510/how-to-spread-django-unit-tests-over-multiple-files
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    #print ' module_name: '+str(module_name)+', is_pkg: '+str(is_pkg)
    module = loader.find_module(module_name).load_module(module_name)
    #print 'dir module: '+str(dir(module))
    for name in dir(module):
        #print 'name: '+str(name)
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, unittest.case.TestCase):
            exec ('%s = obj' % obj.__name__)



old_keys = []
ssh_keys_dir =''

def use_test_key():
    global ssh_keys_dir
    global old_keys
    if 'tests_ssh_key' in os.environ:
        p = Popen(['ssh-add', '-l'], stdout=PIPE, stderr=PIPE)
        (output, err) = p.communicate()
        if err is None or err == '':  # successfull
            lines = output.split('\n')[:-1]
            if len(lines) > 0 and len(lines[0].split(' ')[0]) == 4 \
                and lines[0].split(' ')[3].strip() == '(RSA)':
                
                for line in lines:
                    print 'line: '+str(line.split(' '))
                    k = line.split(' ')[2]
                    old_keys.append(k)
                if len(old_keys) > 0:
                    (ssh_keys_dir, ssh_key_file) = os.path.split(os.environ['tests_ssh_key'])
                    p = Popen(['ssh-add', '-D'], stdout=PIPE,stderr=PIPE)
                    (output, err) = p.communicate()
                    if err is None or err == '' or err.strip()=='All identities removed.':  # deleted successfully
                        p = Popen(['ssh-add',
                                os.environ['tests_ssh_key']],
                                stdout=PIPE, stderr=PIPE)
                        if err is None or err == '' or 'Identity added' in err:
                            print 'Added new key %s successfully'%(os.environ['tests_ssh_key'])
                        else:
                            print 'error adding my key: '+err
                    else:
                        print 'error: '+err
                else:
                    print 'No old keys'
        else:
            print 'error: '+err
    else:
        print 'tests_ssh_key is not there, so it will not change'
        
           
           
def use_old_keys():
    global ssh_keys_dir
    p = Popen(['ssh-add','-D'],stdout=PIPE, stderr=PIPE)
    (output, err) = p.communicate()
    if err is None or err=='' or err.strip()=='All identities removed.':
        print 'The key %s is removed successfully'%(os.environ['tests_ssh_key'])
    else:
        print 'error: '+err
    if len(old_keys) >0:
        for k in old_keys:
            if k.strip() == os.environ['tests_ssh_key']:
                continue
            print 'will add key '+k
            p = Popen(['ssh-add',os.path.join(ssh_keys_dir,k)], stdout=PIPE, stderr=PIPE)
            (output, err) = p.communicate()
            if err is None or err=="" or 'Identity added' in err:
                print 'Added old key %s successfully'%(k)
            else:
                print 'error: '+err

                
    
    
    
           
class NoSQLTestRunner(DjangoTestSuiteRunner):
    def setup_databases(self):
        settings.TEST = True
        print 'I just set TEST to true'
        use_test_key()
        pass
    def teardown_databases(self, *args):
        use_old_keys()
        pass


class NoSQLTestCase(TestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass
    









# 
# class LocalRepoTestCase(TestCase):
#     def setUp(self):   
#     #def __init__(self):
#         self.test_repo = os.environ['test_repo']
#         self.test_ont_hl = os.environ['test_ont_hl']
#         self.test_ont_nl = os.environ['test_ont_nl']
#         self.test_folder = os.environ['test_folder']
#         self.test_ont_hl_abs = os.path.join(self.test_folder,self.test_ont_hl)
#         self.test_ont_nl_abs = os.path.join(self.test_folder,self.test_ont_nl)
#         self.username = os.environ['user_github_username']
#         self.password = os.environ['user_github_password']
#         self.g = Github(self.username,self.password)
#         self.collaborator=autoncore.ToolUser
#         self.notification_url='http://127.0.0.1:8000/'
#         
#         
#     def pushChanges(self):# I need to verify if the commands is executed successfully
#         gu = "git config  user.email \"%s\";" %(self.username)
#         gu+= "git config  user.name \"%s\" ;" %(self.username.split('@')[0])
#         comm =  "cd "+self.test_folder+";"+gu+" git add . "    
#         print comm
#         call(comm,shell=True)
#         comm = "cd "+self.test_folder+";"+gu+" git commit -m 'automation test' "
#         print comm
#         call(comm,shell=True)
#         gup = "git config push.default matching;"
#         comm =  "cd "+self.test_folder+";"+gu+gup+" git push "
#         print comm
#         call(comm,shell=True)
#         time.sleep(15)
#      
# 
#     def getRepo(self):
#         return self.g.get_repo(self.test_repo)
#         
#     
#     def addWebhook(self):
#         self.removeWebhook()
#         res = autoncore.add_webhook(self.test_repo,self.notification_url,self.g)
#         if 'error' not in res:
#             res['error'] ='just for now'
#         self.assertTrue(res['status'],res['error'])
#         
#         
#     def removeWebhook(self):
#         #res = True
#         for hook in self.getRepo().get_hooks():
#             print 'hook_url: '+hook.url
#             if self.notification_url in hook.config['url']:
#                 print 'will delete: '+hook.config['url']
#                 hook.delete()
#             else:
#                 print 'not match: '+hook.config['url']   
#                 #res = True
#                 #break
#         #self.assertTrue(res,'Webhook does not exists')    
#         
#     
#     def addCollaborator(self):
#         g_auth_user = self.g.get_user()# this to get authenticated if login is not passed
#         # and add collaborator expects NamedUser
#         res = autoncore.add_collaborator(self.test_repo,self.g.get_user(g_auth_user.login),self.g)
#         if 'error' not in res:
#             res['error'] = 'this error should not be showen'
#         self.assertTrue(res['status'], res['error'])
#         
#     
#     def removeCollaborator(self):
#         self.getRepo().remove_from_collaborators(self.collaborator)
#         
#         
#     def updateOntologies(self):
#         text_flag = '<!--Automated test1-->'
#         text_alternative_flag='<!--Automated test2-->'
#         with open(self.test_ont_hl_abs,'w+') as f:
#             for line in f:
#                 if text_flag in line:
#                     f.seek(-len(text_flag),os.SEEK_END)
#                     f.write(text_alternative_flag)
#                     break
#                 elif text_alternative_flag in line:
#                     f.seek(-len(text_alternative_flag),os.SEEK_END)
#                     f.write(text_flag)
#                     break
#                 
#         with open(self.test_ont_nl_abs,'w+') as f:
#             for line in f:
#                 if text_flag in line:
#                     f.seek(-len(text_flag),os.SEEK_END)
#                     f.write(text_alternative_flag)
#                     break
#                 elif text_alternative_flag in line:
#                     f.seek(-len(text_alternative_flag),os.SEEK_END)
#                     f.write(text_flag)
#                     break
#         
#      
#         
#     def _fixture_setup(self):
#         return
# 
#     def _fixture_teardown(self):
#         return

