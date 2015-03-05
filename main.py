#!/usr/bin/python
import sys
from github import Github
import getpass
user = None
password = None

if len(sys.argv)!=3:
	user =  raw_input("Enter your email: ")
	password = getpass.getpass("Enter your password: ")	
else:
	user = sys.argv[1]
	password = sys.argv[2]
g = Github(user,password)
for repo in g.get_user().get_repos():
    print repo.name


