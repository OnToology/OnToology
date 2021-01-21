
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
repo_name_with_res = "ontoology-auto-test-with-res"
repo = user + "/" + repo_name
repo_with_res = user + "/" + repo_name_with_res
ontology_name = "alo.owl"
branch = "master"


mock_dict_success = {
    "/repos/%s" % repo: {
        "GET": {
            "status": 200,
            "body": get_repo_dict(repo)
        }
    },
    "/repos/%s" % repo_with_res: {
        "GET": {
            "status": 200,
            "body": get_repo_dict(repo_with_res)
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
    },
    "/repos/%s/collaborators/%s" % (repo,user) : {
        # "GET": {
        #     "status": 204,
        #     "body": ""
        # },
        "GET": {
            "status": 404,
            "body": ""
        },
        "PUT": {
            "status": 201,
            "body": get_add_collaborator_dict(repo)
        }
    },
    "/repos/%s/contents/OnToology/%s/documentation/.htaccess" % (repo_with_res, ontology_name): {
        "GET": {
            "status": 200,
            "body": get_file_content_dict(repo_with_res, branch, "OnToology/%s/documentation/.htaccess" % ontology_name)
        },
        "PUT": {
            "status": 200,
            "body": get_update_content_dict(repo_with_res, branch, "OnToology/%s/documentation/.htaccess" % ontology_name)
        }
    },
    "/user/repository_invitations/%s" % "1" :{
        "PATCH": {
            "status": 204,
            "body": ""
        }
    }
}

mock_dict = {
    'success': mock_dict_success
}