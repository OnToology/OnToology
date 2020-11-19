
from .commit import *
from .fork import *
from .org import *
from .pull import *
from .repo import *
from .tree import *
from .user import *
from .milestone import *

user = "ahmad88me"
repo_name = "ontoology-auto-test-no-res"
repo = user + "/" + repo_name

mock_dict_success = {
    "/repos/%s" % repo: {
        "GET": {
            "status": 200,
            "body": get_repo_dict(repo)
        }
    },
    "/user": {
        "GET": {
            "status": 200,
            "body": get_auth_user_dict(user),
        }
    },
    "/users/%s" % user: {
        "GET": {
            "status": 200,
            "body": get_user_dict(user),
        }
    },
    "/repos/%s/commits" % repo: {
        "GET": {
            "status": 200,
            "body": get_commits_dict(repo),
        }
    },
    "/repos/%s/git/trees/6dcb09b5b57875f334f61aebed695e2e4193db5e" % repo: {
        "GET": {
            "status": 200,
            "body": get_tree_dict()
        }
    },
    "/repos/%s/forks" % repo:{
        "POST": {
            "status": 202,
            "body": get_fork_dict(repo)
        }
    },
    "/repos/%s/pulls" % repo: {
        "GET":{
            "status": 200,
            "body": get_pulls_dict(repo, branch="master") # regardless of the branch. It always pass
        },
        "POST": {
            "status": 201,
            "body": get_pulls_dict(repo, branch="master")[0]
        }
    }
}

mock_dict = {
    'success': mock_dict_success
}