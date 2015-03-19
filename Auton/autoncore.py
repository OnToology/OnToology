#!/usr/bin/python
import sys, os
from github import Github
import getpass
from datetime import datetime
from subprocess import call
import string, random
import time

parent_folder = None



home = '/home/ubuntu/temp/'
#home = '/Users/blakxu/test123/pro/'


g = None


def git_magic(target_repo,user,cloning_repo,changed_files):
    global g
    global parent_folder
    parent_folder = user
    print '############################### magic #############################'
    #so the tool user can takeover and do stuff
    username = os.environ['github_username']
    password = os.environ['github_password']
    g = Github(username,password)
    local_repo = target_repo.replace(target_repo.split('/')[-2] ,'AutonUser')#target_repo.replace(cloning_repo.split('/')[-2],username)
    delete_repo(local_repo)
    #print 'repo deleted'
    fork_repo(target_repo,username,password)
    print 'repo forked'
#     cloning_repo = cloning_repo.replace(cloning_repo.split('/')[-2],username)
    clone_repo(cloning_repo,user)
    print 'repo cloned'
    update_readme(changed_files,cloning_repo,user)
    print 'readme updated'
    commit_changes()
    print 'changes committed'
    remove_old_pull_requests(target_repo)
    r = send_pull_request(local_repo,'AutonUser')
    print 'pull request is sent'
    return r



def delete_repo(local_repo):
    try:
        g.get_repo(local_repo).delete()
        print 'repo deleted '
    except:
        print 'the repo doesn\'t exists [not an error]'


def fork_repo(target_repo,username,password):
    time.sleep(5)#the wait time to give github sometime so the repo can be forked successfully
    #this is a workaround and not a proper way to do a fork
    comm = "curl --user \"%s:%s\" --request POST --data \'{}\' https://api.github.com/repos/%s/forks" % (username,password,target_repo)
    call(comm,shell=True)
    print 'fork'
    
    


def clone_repo(cloning_repo,user):
    
    time.sleep(5)#the wait time to give github sometime so the repo can be cloned
    print "rm"," -Rf "+home+parent_folder
    call("rm"+" -Rf "+home+parent_folder, shell=True)
    print "git"+" clone"+" "+cloning_repo+" "+home+parent_folder
    call("git"+" clone"+" "+cloning_repo+" "+home+parent_folder, shell=True)
    print "chmod 777 -R "+home+parent_folder
    call("chmod 777 -R "+home+parent_folder, shell=True)



                
def update_readme(changed_files,cloning_repo,user):
    for i in range(3):
        try:
            f = open(home+parent_folder+"/"+"README.md","a")
            break
        except IOError:
            print 'readme is not ready: '+str(i)
            time.sleep(5)
            clone_repo(cloning_repo,user)
    f.write("\n##Changelog "+str(datetime.today())+"\n")
    for chf in changed_files:
        f.write("\n* "+chf)                
    f.close()
                




def commit_changes():
    gu = ""
    gu = "git config  user.email \"ahmad88csc@gmail.com\";"
    gu+="git config  user.name \"AutonUser\" ;"
    print "command: "+"cd "+home+parent_folder+";"+gu+" git add README.md "    
    call("cd "+home+parent_folder+";"+gu+" git add README.md ",shell=True)
    print "cd "+home+parent_folder+";"+gu+" git commit -m 'automated change' "
    call("cd "+home+parent_folder+";"+gu+" git commit -m 'automated change' ",shell=True)
    gup =""
    gup = "git config push.default matching;"
    print "cd "+home+parent_folder+";"+gu+gup+" git push "
    call("cd "+home+parent_folder+";"+gu+gup+" git push ",shell=True)




# def push_repo():
# #    commit_changes()
#     call("cd "+home+parent_folder+"/"+"; git push ",shell=True)
#                 




def refresh_repo(target_repo):
    local_repo = target_repo.split('/')[-1]
    g.get_user().get_repo(local_repo).delete()
    g.get_user().create_fork(target_repo)




def remove_old_pull_requests(target_repo):
    title = 'AutonTool update'
    for p in g.get_repo(target_repo).get_pulls():
        if p.title == title:
            p.edit(state="closed")
    



def send_pull_request(target_repo,username):
    title = 'AutonTool update'
    body = title
    try:
        g.get_repo(target_repo).create_pull(head=username+':master',base='master',title=title,body=body)
        return 'pull request created successfully'
    except Exception as e:
        return str(e.data)




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




