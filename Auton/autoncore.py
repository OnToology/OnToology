#!/usr/bin/python
import sys, os
from github import Github
import getpass
from datetime import datetime
from subprocess import call
import string, random


parent_folder = None



home = '/home/ubuntu/temp/'
#home = '/Users/blakxu/test123/pro/'


g = None


def git_magic(target_repo,user,cloning_repo,changed_files):
    global g
    global parent_folder
    parent_folder = user
    #so the tool user can takeover and do stuff
    username = os.environ['github_username']
    password = os.environ['github_password']
    g = Github(username,password)
    fork_repo(target_repo,username,password)
    print 'repo forked'
    cloning_repo = cloning_repo.replace(cloning_repo.split('/')[-2],username)
    clone_repo(cloning_repo)
    print 'repo cloned'
    update_readme(changed_files)
    print 'readme updated'
    commit_changes()
    print 'changes committed'
    send_pull_request(target_repo,username)
    print 'pull request is sent'
    return changed_files




def fork_repo(target_repo,username,password):
    #this is a workaround and not a proper way to do a fork
    comm = "curl --user \"%s:%s\" --request POST --data \'{}\' https://api.github.com/repos/%s/forks" % (username,password,target_repo)
    call(comm,shell=True)
    print 'fork'
    
    


def clone_repo(cloning_repo):
    call(["rm","-Rf",home+parent_folder])
    call(["git","clone",cloning_repo,home+parent_folder])




                
def update_readme(changed_files):
    f = open(home+parent_folder+"/"+"README.md","a")
    f.write("\n##Changelog "+str(datetime.today())+"\n")
    for chf in changed_files:
        f.write("\n* "+chf)                
    f.close()
                




def commit_changes():
    print "command: "+"git --git-dir="+home+parent_folder+"/"+".git add "+home+parent_folder+"/README.md "
    
    gu = "git config  user.email \"ahmad88csc@gmail.com\";"
    gu+="git config  user.name \"AutonUser\" ;"
    call("cd "+home+parent_folder+";"+gu+" git add README.md ",shell=True)
    call("cd "+home+parent_folder+";"+gu+" git commit -m 'automated change' ",shell=True)
    gup = "git config push.default simple;"
    call("cd "+home+parent_folder+";"+gu+gup+" git push ",shell=True)




# def push_repo():
# #    commit_changes()
#     call("cd "+home+parent_folder+"/"+"; git push ",shell=True)
#                 




def refresh_repo(target_repo):
    local_repo = target_repo.split('/')[-1]
    g.get_user().get_repo(local_repo).delete()
    g.get_user().create_fork(target_repo)





def send_pull_request(target_repo,username):
    title = 'AutonTool update'
    body = title
    g.get_repo(target_repo).create_pull(head=username+':master',base='master',title=title,body=body)
    




def webhook_access(client_id,redirect_url):
    scope = 'admin:org_hook'
    scope+=',admin:org,admin:public_key,admin:repo_hook,gist,notifications,delete_repo,repo_deployment,repo,public_repo,user,admin:public_key'
    sec = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(9)])
    return "https://github.com/login/oauth/authorize?client_id="+client_id+"&redirect_uri="+redirect_url+"&scope="+scope+"&state="+sec, sec






def add_webhook(target_repo,notification_url):
    name = "web"
    active = True
    events = ["push"]
    config = {
               "url": notification_url,
               "content_type": "form"
    }
    try:
        g.get_repo(target_repo).create_hook(name,config,events,active)
        return {'status': True}
    except Exception as e:
        return {'status': False, 'error': e.data}



def add_collaborator(target_repo,user):
    try:
        g.get_repo(target_repo).add_to_collaborators(user)
        return {'status': True}
    except Exception as e:
        return {'status': False, 'error': e.data}



def update_g(token):
    global g
    g = Github(token)




