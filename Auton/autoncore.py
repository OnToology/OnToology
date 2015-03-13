#!/usr/bin/python
import sys, os
from github import Github
import getpass
from datetime import datetime
from subprocess import call

user = os.environ['github_username']
password = os.environ['github_password']
#target_repo = 'ahmad88me/target'

#home = '/Users/blakxu/Studying Material UPM/Thesis/code/'
home = '/Users/blakxu/test123/pro/'


parent_folder = None
project_folder = None

# if len(sys.argv)!=3:
#     user =  raw_input("Enter your email: ")
#     password = getpass.getpass("Enter your password: ")    
# else:
#     user = sys.argv[1]
#     password = sys.argv[2]
g = Github(user,password)
#for repo in g.get_user().get_repos():
#    print repo.name
# repo = g.get_repo(target_repo)
# print repo.name
# for c in repo.get_commits(since=datetime(year=2015,month=3,day=5,hour=17,minute=15,second=0)):
#     print c.sha
#     for f in c.files:
#         print "--> "+f.filename



# def git_magic(target_repo,last_commit_date,user,cloning_repo):
#     global parent_folder
#     global project_folder
#     parent_folder = user
#     project_folder = target_repo.split("/")[-1]
#     changed_files = get_updated_files(target_repo, last_commit_date)
#     print 'got updated files'
#     clone_repo(cloning_repo)
#     print 'repo cloned'
#     update_readme(changed_files)
#     print 'readme updated'
#     #push_repo()
#     #print 'repo pull request'
#     commit_changes()
#     print 'changes committed'
#     send_pull_request(cloning_repo)
#     print 'pull request is sent'
#     return changed_files



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
    

#def add_as_collaborator(target_repo):
#    g_ahmad.get_repo(target_repo).add_to_collaborators('Autontool')
    #g.get_repo(target_repo).add_to_collaborators(collaborator)


#https://github.com/login/oauth/authorize?client_id=bbfc39dd5b6065bbe53b&redirect_uri=http://127.0.0.1:8000&scope=repo&state=213498549ksdjflkjadslaksfd
#from datetime import datetime
#target_repo = 'ahmad88me/target'
#target_datetime = datetime.today()
#user = 'ahmad88me@gmail.com'
#git_magic(target_repo, target_datetime,user,'git@github.com:'+target_repo+'.git')


