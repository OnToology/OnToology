#!/usr/bin/python
import sys, os
from github import Github
import getpass
from datetime import datetime
from subprocess import call
import string, random


parent_folder = None
project_folder = None
home = '/home/ubuntu/temp/'

user = os.environ['github_username']
password = os.environ['github_password']

g = Github(user,password)


def git_magic(target_repo,user,cloning_repo,changed_files):
    global parent_folder
    global project_folder
    parent_folder = user
    project_folder = target_repo.split("/")[-1]
    clone_repo(cloning_repo)
    print 'repo cloned'
    update_readme(changed_files)
    print 'readme updated'
    commit_changes()
    print 'changes committed'
    send_pull_request(cloning_repo)
    print 'pull request is sent'
    return changed_files











def get_updated_files(target_repo,last_commit_date):
    changed_files = []
    repo = g.get_repo(target_repo)
    for commit in repo.get_commits(since=last_commit_date):
        for f in commit.files:
            if f not in changed_files:# to avoid duplicates
                changed_files.append(f.filename)
    return set(changed_files)          




def clone_repo(cloning_repo):
    call(["rm","-Rf",home+parent_folder])
    call(["git","clone",cloning_repo,home+parent_folder])
    #call("export HOME=/home/ubuntu; git"+" clone "+cloning_repo+" "+home+parent_folder)




                
def update_readme(changed_files):
    f = open(home+parent_folder+"/"+"README.md","a")
    f.write("\n##Changelog "+str(datetime.today())+"\n")
    for chf in changed_files:
        f.write("\n* "+chf)                
    f.close()
                




def commit_changes():
    print "command: "+"git --git-dir="+home+parent_folder+"/"+".git add "+home+parent_folder+"/README.md "
    call("cd "+home+parent_folder+"/"+"; git add "+home+parent_folder+"/README.md ",shell=True)
    call("cd "+home+parent_folder+"/"+"; git commit -m 'automated change' ",shell=True)




def push_repo():
    commit_changes()
    call("cd "+home+parent_folder+"/"+"; git push ",shell=True)
                


def refresh_repo(target_repo):
    local_repo = target_repo.split('/')[-1]
    g.get_user().get_repo(local_repo).delete()
    g.get_user().create_fork(target_repo)



def send_pull_request(cloning_repo):
    title = 'AutonTool update'
    body = title
    source_repo = (cloning_repo.split(':')[-1])[:-4]
    print 'source_repo: '+source_repo
    g.get_repo(source_repo).create_pull(head='Autontool:master',base='master',title=title,body=body)
    


def webhook_access(redirect_url):
    client_id='bbfc39dd5b6065bbe53b'
    #redirect_url = 'http://www.familyyard.net/attach_webhook'
    scope = 'admin:org_hook'
    scope+=',admin:org,admin:public_key,admin:repo_hook,gist,notifications,delete_repo,repo_deployment,repo,public_repo,user,admin:public_key,admin'
    sec = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(9)])
    return "https://github.com/login/oauth/authorize?client_id="+client_id+"&redirect_uri="+redirect_url+"&scope="+scope+"&state="+sec, sec



def add_webhook(target_repo,notification_url):
    name = "web"
    active = True
    events = ["push"]
    #notificatoin_url = "http://familyyard.com/attach_webhook"
    config = {
               "url": notification_url,
               "content_type": "json"
    }
    g.get_repo(target_repo).create_hook(name,config,events,active)


# 
# name = "autonhook"
# active = True
# events = ["push"]
# config = {
#            "url": notification_url,
#            "content_type": "form"
# }
# config = {
#            "url": notification_url,
#            "content_type": "json"
# }
# g.get_repo(target_repo).create_hook(name,config,events,active)



#def add_as_collaborator(target_repo):
#    g_ahmad.get_repo(target_repo).add_to_collaborators('Autontool')
    #g.get_repo(target_repo).add_to_collaborators(collaborator)


#https://github.com/login/oauth/authorize?client_id=bbfc39dd5b6065bbe53b&redirect_uri=http://127.0.0.1:8000&scope=repo&state=213498549ksdjflkjadslaksfd
#from datetime import datetime
#target_repo = 'ahmad88me/target'
#target_datetime = datetime.today()
#user = 'ahmad88me@gmail.com'
#git_magic(target_repo, target_datetime,user,'git@github.com:'+target_repo+'.git')


