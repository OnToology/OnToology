#!/usr/bin/python
import sys
from github import Github
import getpass
from datetime import datetime
user = 'ahmad88me@gmail.com'
password = '000000Ul.'
target_repo = 'ahmad88me/target'
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

def get_updated_files(target_repo,last_commit_date):
    changed_files = []
    repo = g.get_repo(target_repo)
    for commit in repo.get_commits(since=last_commit_date):
        for f in commit.files:
            if f not in changed_files:# to avoid duplicates
                changed_files.append(f.filename)
    return changed_files          


                
                
                
                
                
                
                
                
                
                
