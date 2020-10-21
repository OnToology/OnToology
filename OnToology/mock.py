def get_parent_dict(repo):
    user, name = repo.split("/")
    parent_dict = {
        "id": 1296269,
        "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
        "name": name,
        "full_name": repo,
        "owner": {
            "login": user,
            "id": 1,
            "node_id": "MDQ6VXNlcjE=",
            "avatar_url": "https://github.com/images/error/%s_happy.gif" % user,
            "gravatar_id": "",
            "url": "https://api.github.com/users/%s" % user,
            "html_url": "https://github.com/%s" % user,
            "followers_url": "https://api.github.com/users/%s/followers" % user,
            "following_url": "https://api.github.com/users/%s/following{/other_user}" % user,
            "gists_url": "https://api.github.com/users/%s/gists{/gist_id}" % user,
            "starred_url": "https://api.github.com/users/%s/starred{/owner}{/repo}" % user,
            "subscriptions_url": "https://api.github.com/users/%s/subscriptions" % user,
            "organizations_url": "https://api.github.com/users/%s/orgs" % user,
            "repos_url": "https://api.github.com/users/%s/repos" % user,
            "events_url": "https://api.github.com/users/%s/events{/privacy}" % user,
            "received_events_url": "https://api.github.com/users/%s/received_events" % user,
            "type": "User",
            "site_admin": False
        },
        "private": False,
        "html_url": "https://github.com/%s" % repo,
        "description": "This your first repo!",
        "fork": False,
        "url": "https://api.github.com/repos/%s" % repo,
        "archive_url": "http://api.github.com/repos/%s/{archive_format}{/ref}" % repo,
        "assignees_url": "http://api.github.com/repos/%s/assignees{/user}" % repo,
        "blobs_url": "http://api.github.com/repos/%s/git/blobs{/sha}" % repo,
        "branches_url": "http://api.github.com/repos/%s/branches{/branch}" % repo,
        "collaborators_url": "http://api.github.com/repos/%s/collaborators{/collaborator}" % repo,
        "comments_url": "http://api.github.com/repos/%s/comments{/number}" % repo,
        "commits_url": "http://api.github.com/repos/%s/commits{/sha}" % repo,
        "compare_url": "http://api.github.com/repos/%s/compare/{base}...{head}" % repo,
        "contents_url": "http://api.github.com/repos/%s/contents/{+path}" % repo,
        "contributors_url": "http://api.github.com/repos/%s/contributors" % repo,
        "deployments_url": "http://api.github.com/repos/%s/deployments" % repo,
        "downloads_url": "http://api.github.com/repos/%s/downloads" % repo,
        "events_url": "http://api.github.com/repos/%s/events" % repo,
        "forks_url": "http://api.github.com/repos/%s/forks" % repo,
        "git_commits_url": "http://api.github.com/repos/%s/git/commits{/sha}" % repo,
        "git_refs_url": "http://api.github.com/repos/%s/git/refs{/sha}" % repo,
        "git_tags_url": "http://api.github.com/repos/%s/git/tags{/sha}" % repo,
        "git_url": "git:github.com/%s.git" % repo,
        "issue_comment_url": "http://api.github.com/repos/%s/issues/comments{/number}" % repo,
        "issue_events_url": "http://api.github.com/repos/%s/issues/events{/number}" % repo,
        "issues_url": "http://api.github.com/repos/%s/issues{/number}" % repo,
        "keys_url": "http://api.github.com/repos/%s/keys{/key_id}" % repo,
        "labels_url": "http://api.github.com/repos/%s/labels{/name}" % repo,
        "languages_url": "http://api.github.com/repos/%s/languages" % repo,
        "merges_url": "http://api.github.com/repos/%s/merges" % repo,
        "milestones_url": "http://api.github.com/repos/%s/milestones{/number}" % repo,
        "notifications_url": "http://api.github.com/repos/%s/notifications{?since,all,participating}" % repo,
        "pulls_url": "http://api.github.com/repos/%s/pulls{/number}" % repo,
        "releases_url": "http://api.github.com/repos/%s/releases{/id}" % repo,
        "ssh_url": "git@github.com:%s.git" % repo,
        "stargazers_url": "http://api.github.com/repos/%s/stargazers" % repo,
        "statuses_url": "http://api.github.com/repos/%s/statuses/{sha}" % repo,
        "subscribers_url": "http://api.github.com/repos/%s/subscribers" % repo,
        "subscription_url": "http://api.github.com/repos/%s/subscription" % repo,
        "tags_url": "http://api.github.com/repos/%s/tags" % repo,
        "teams_url": "http://api.github.com/repos/%s/teams" % repo,
        "trees_url": "http://api.github.com/repos/%s/git/trees{/sha}" % repo,
        "clone_url": "https://github.com/%s.git" % repo,
        "mirror_url": "git:git.example.com/%s" % repo,
        "hooks_url": "http://api.github.com/repos/%s/hooks" % repo,
        "svn_url": "https://svn.github.com/%s" % repo,
        "homepage": "https://github.com",
        "language": None,
        "forks_count": 9,
        "stargazers_count": 80,
        "watchers_count": 80,
        "size": 108,
        "default_branch": "master",
        "open_issues_count": 0,
        "is_template": True,
        "topics": [
            "octocat",
            "atom",
            "electron",
            "api"
        ],
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "has_pages": False,
        "has_downloads": True,
        "archived": False,
        "disabled": False,
        "visibility": "public",
        "pushed_at": "2011-01-26T19:06:43Z",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2011-01-26T19:14:43Z",
        "permissions": {
            "admin": False,
            "push": False,
            "pull": True
        },
        "allow_rebase_merge": True,
        "template_repository": None,
        "temp_clone_token": "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
        "allow_squash_merge": True,
        "delete_branch_on_merge": True,
        "allow_merge_commit": True,
        "subscribers_count": 42,
        "network_count": 0
    }
    return parent_dict


def get_commits_dict(repo):
    user, name = repo.split("/")
    commits_dict = [
        {
            "url": "https://api.github.com/repos/%s/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e" % repo,
            "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
            "node_id": "MDY6Q29tbWl0NmRjYjA5YjViNTc4NzVmMzM0ZjYxYWViZWQ2OTVlMmU0MTkzZGI1ZQ==",
            "html_url": "https://github.com/%s/commit/6dcb09b5b57875f334f61aebed695e2e4193db5e" % repo,
            "comments_url": "https://api.github.com/repos/%s/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e/comments" % repo,
            "commit": {
                "url": "https://api.github.com/repos/%s/git/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e" % repo,
                "author": {
                    "name": "Monalisa Octocat",
                    "email": "support@github.com",
                    "date": "2011-04-14T16:00:49Z"
                },
                "committer": {
                    "name": "Monalisa Octocat",
                    "email": "support@github.com",
                    "date": "2011-04-14T16:00:49Z"
                },
                "message": "Fix all the bugs",
                "tree": {
                    "url": "https://api.github.com/repos/%s/tree/6dcb09b5b57875f334f61aebed695e2e4193db5e" % repo,
                    "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
                },
                "comment_count": 0,
                "verification": {
                    "verified": False,
                    "reason": "unsigned",
                    "signature": None,
                    "payload": None
                }
            },
            "author": get_auth_user_dict(user),
            "committer": get_auth_user_dict(user),
            "parents": [
                {
                    "url": "https://api.github.com/repos/%s/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e" % repo,
                    "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
                }
            ]
        }
    ]
    return commits_dict


def get_auth_user_dict(user):
    a_user_dict = {
        "login": user,
        "id": 1,
        "node_id": "MDQ6VXNlcjE=",
        "avatar_url": "https://github.com/images/error/%s_happy.gif" % user,
        "gravatar_id": "",
        "url": "https://api.github.com/users/%s" % user,
        "html_url": "https://github.com/%s" % user,
        "followers_url": "https://api.github.com/users/%s/followers" % user,
        "following_url": "https://api.github.com/users/%s/following{/other_user}" % user,
        "gists_url": "https://api.github.com/users/%s/gists{/gist_id}" % user,
        "starred_url": "https://api.github.com/users/%s/starred{/owner}{/repo}" % user,
        "subscriptions_url": "https://api.github.com/users/%s/subscriptions" % user,
        "organizations_url": "https://api.github.com/users/%s/orgs" % user,
        "repos_url": "https://api.github.com/users/%s/repos" % user,
        "events_url": "https://api.github.com/users/%s/events{/privacy}" % user,
        "received_events_url": "https://api.github.com/users/%s/received_events" % user,
        "type": "User",
        "site_admin": False,
        "name": "monalisa %s" % user,
        "company": "GitHub",
        "blog": "https://github.com/blog",
        "location": "San Francisco",
        "email": "%s@github.com" % user,
        "hireable": False,
        "bio": "There once was...",
        "twitter_username": "%s" % user,
        "public_repos": 2,
        "public_gists": 1,
        "followers": 20,
        "following": 0,
        "created_at": "2008-01-14T04:33:35Z",
        "updated_at": "2008-01-14T04:33:35Z",
        "private_gists": 81,
        "total_private_repos": 100,
        "owned_private_repos": 100,
        "disk_usage": 10000,
        "collaborators": 8,
        "two_factor_authentication": True,
        "plan": {
            "name": "Medium",
            "space": 400,
            "private_repos": 20,
            "collaborators": 0
        }
    }


def get_user_dict(user):
    user_dict = {
        "login": user,
        "id": 1,
        "node_id": "MDQ6VXNlcjE=",
        "avatar_url": "https://github.com/images/error/%s_happy.gif" % user,
        "gravatar_id": "",
        "url": "https://api.github.com/users/%s" % user,
        "html_url": "https://github.com/%s" % user,
        "followers_url": "https://api.github.com/users/%s/followers" % user,
        "following_url": "https://api.github.com/users/%s/following{/other_user}" % user,
        "gists_url": "https://api.github.com/users/%s/gists{/gist_id}" % user,
        "starred_url": "https://api.github.com/users/%s/starred{/owner}{/repo}" % user,
        "subscriptions_url": "https://api.github.com/users/%s/subscriptions" % user,
        "organizations_url": "https://api.github.com/users/%s/orgs" % user,
        "repos_url": "https://api.github.com/users/%s/repos" % user,
        "events_url": "https://api.github.com/users/%s/events{/privacy}" % user,
        "received_events_url": "https://api.github.com/users/%s/received_events" % user,
        "type": "User",
        "site_admin": False,
        "name": "monalisa ahmad88me",
        "company": "GitHub",
        "blog": "https://github.com/blog",
        "location": "San Francisco",
        "email": "%s@gmail.com" % user,
        "hireable": False,
        "bio": "There once was...",
        "twitter_username": "%s" % user,
        "public_repos": 2,
        "public_gists": 1,
        "followers": 20,
        "following": 0,
        "created_at": "2008-01-14T04:33:35Z",
        "updated_at": "2008-01-14T04:33:35Z",
    }
    return user_dict


def get_repo_dict(repo):
    user, name = repo.split("/")
    repo_dict = {
        "id": 1296269,
        "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
        "name": name,
        "full_name": "%s" % repo,
        "owner": {
            "login": user,
            "id": 1,
            "node_id": "MDQ6VXNlcjE=",
            "avatar_url": "https://github.com/images/error/%s_happy.gif" % user,
            "gravatar_id": "",
            "url": "https://api.github.com/users/%s" % user,
            "html_url": "https://github.com/%s" % user,
            "followers_url": "https://api.github.com/users/%s/followers" % user,
            "following_url": "https://api.github.com/users/%s/following{/other_user}" % user,
            "gists_url": "https://api.github.com/users/%s/gists{/gist_id}" % user,
            "starred_url": "https://api.github.com/users/%s/starred{/owner}{/repo}" % user,
            "subscriptions_url": "https://api.github.com/users/%s/subscriptions" % user,
            "organizations_url": "https://api.github.com/users/%s/orgs" % user,
            "repos_url": "https://api.github.com/users/%s/repos" % user,
            "events_url": "https://api.github.com/users/%s/events{/privacy}" % user,
            "received_events_url": "https://api.github.com/users/%s/received_events" % user,
            "type": "User",
            "site_admin": False
        },
        "private": False,
        "html_url": "https://github.com/%s" % repo,
        "description": "This your first repo!",
        "fork": False,
        "url": "https://api.github.com/repos/%s" % repo,
        "archive_url": "http://api.github.com/repos/%s/{archive_format}{/ref}" % repo,
        "assignees_url": "http://api.github.com/repos/%s/assignees{/user}" % repo,
        "blobs_url": "http://api.github.com/repos/%s/git/blobs{/sha}" % repo,
        "branches_url": "http://api.github.com/repos/%s/branches{/branch}" % repo,
        "collaborators_url": "http://api.github.com/repos/%s/collaborators{/collaborator}" % repo,
        "comments_url": "http://api.github.com/repos/%s/comments{/number}" % repo,
        "commits_url": "http://api.github.com/repos/%s/commits{/sha}" % repo,
        "compare_url": "http://api.github.com/repos/%s/compare/{base}...{head}" % repo,
        "contents_url": "http://api.github.com/repos/%s/contents/{+path}" % repo,
        "contributors_url": "http://api.github.com/repos/%s/contributors" % repo,
        "deployments_url": "http://api.github.com/repos/%s/deployments" % repo,
        "downloads_url": "http://api.github.com/repos/%s/downloads" % repo,
        "events_url": "http://api.github.com/repos/%s/events" % repo,
        "forks_url": "http://api.github.com/repos/%s/forks" % repo,
        "git_commits_url": "http://api.github.com/repos/%s/git/commits{/sha}" % repo,
        "git_refs_url": "http://api.github.com/repos/%s/git/refs{/sha}" % repo,
        "git_tags_url": "http://api.github.com/repos/%s/git/tags{/sha}" % repo,
        "git_url": "git:github.com/%s.git" % repo,
        "issue_comment_url": "http://api.github.com/repos/%s/issues/comments{/number}" % repo,
        "issue_events_url": "http://api.github.com/repos/%s/issues/events{/number}" % repo,
        "issues_url": "http://api.github.com/repos/%s/issues{/number}" % repo,
        "keys_url": "http://api.github.com/repos/%s/keys{/key_id}" % repo,
        "labels_url": "http://api.github.com/repos/%s/labels{/name}" % repo,
        "languages_url": "http://api.github.com/repos/%s/languages" % repo,
        "merges_url": "http://api.github.com/repos/%s/merges" % repo,
        "milestones_url": "http://api.github.com/repos/%s/milestones{/number}" % repo,
        "notifications_url": "http://api.github.com/repos/%s/notifications{?since,all,participating}" % repo,
        "pulls_url": "http://api.github.com/repos/%s/pulls{/number}" % repo,
        "releases_url": "http://api.github.com/repos/%s/releases{/id}" % repo,
        "ssh_url": "git@github.com:%s.git" % repo,
        "stargazers_url": "http://api.github.com/repos/%s/stargazers" % repo,
        "statuses_url": "http://api.github.com/repos/%s/statuses/{sha}" % repo,
        "subscribers_url": "http://api.github.com/repos/%s/subscribers" % repo,
        "subscription_url": "http://api.github.com/repos/%s/subscription" % repo,
        "tags_url": "http://api.github.com/repos/%s/tags" % repo,
        "teams_url": "http://api.github.com/repos/%s/teams" % repo,
        "trees_url": "http://api.github.com/repos/%s/git/trees{/sha}" % repo,
        "clone_url": "https://github.com/%s.git" % repo,
        "mirror_url": "git:git.example.com/%s" % repo,
        "hooks_url": "http://api.github.com/repos/%s/hooks" % repo,
        "svn_url": "https://svn.github.com/%s" % repo,
        "homepage": "https://github.com",
        "language": None,
        "forks_count": 9,
        "stargazers_count": 80,
        "watchers_count": 80,
        "size": 108,
        "default_branch": "master",
        "open_issues_count": 0,
        "is_template": True,
        "topics": [
            "octocat",
            "atom",
            "electron",
            "api"
        ],
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "has_pages": False,
        "has_downloads": True,
        "archived": False,
        "disabled": False,
        "visibility": "public",
        "pushed_at": "2011-01-26T19:06:43Z",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2011-01-26T19:14:43Z",
        "permissions": {
            "pull": True,
            "triage": True,
            "push": False,
            "maintain": False,
            "admin": False
        },
        "allow_rebase_merge": True,
        "template_repository": None,
        "temp_clone_token": "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
        "allow_squash_merge": True,
        "delete_branch_on_merge": True,
        "allow_merge_commit": True,
        "subscribers_count": 42,
        "network_count": 0,
        "license": get_license_dict(),
        "organization": get_organization_dict(name),
        "parent": get_parent_dict(repo),
        "source": get_parent_dict(repo)
    }
    return repo_dict


def get_license_dict():
    license = {
        "key": "mit",
        "name": "MIT License",
        "spdx_id": "MIT",
        "url": "https://api.github.com/licenses/mit",
        "node_id": "MDc6TGljZW5zZW1pdA==",
    }
    return license


def get_organization_dict(name):
    organization = {
        "login": name,
        "id": 1,
        "node_id": "MDQ6VXNlcjE=",
        "avatar_url": "https://github.com/images/error/%s_happy.gif" % name,
        "gravatar_id": "",
        "url": "https://api.github.com/users/%s" % name,
        "html_url": "https://github.com/%s" % name,
        "followers_url": "https://api.github.com/users/%s/followers" % name,
        "following_url": "https://api.github.com/users/%s/following{/other_user}" % name,
        "gists_url": "https://api.github.com/users/%s/gists{/gist_id}" % name,
        "starred_url": "https://api.github.com/users/%s/starred{/owner}{/repo}" % name,
        "subscriptions_url": "https://api.github.com/users/%s/subscriptions" % name,
        "organizations_url": "https://api.github.com/users/%s/orgs" % name,
        "repos_url": "https://api.github.com/users/%s/repos" % name,
        "events_url": "https://api.github.com/users/%s/events{/privacy}" % name,
        "received_events_url": "https://api.github.com/users/%s/received_events" % name,
        "type": "Organization",
        "site_admin": False,
    }
    return organization


def get_tree_dict():
    tree = {
        "sha": "9fb037999f264ba9a7fc6274d15fa3ae2ab98312",
        "url": "https://api.github.com/repos/octocat/Hello-World/trees/9fb037999f264ba9a7fc6274d15fa3ae2ab98312",
        "tree": [
            {
                "path": "geolinkeddata.owl",
                "mode": "100644",
                "type": "blob",
                "size": 30,
                "sha": "44b4fc6d56897b048c772eb4087f854f46256132",
                "url": "https://api.github.com/repos/octocat/Hello-World/git/blobs/44b4fc6d56897b048c772eb4087f854f46256132"
            },
            {
                "path": "subdir",
                "mode": "040000",
                "type": "tree",
                "sha": "f484d249c660418515fb01c2b9662073663c242e",
                "url": "https://api.github.com/repos/octocat/Hello-World/git/blobs/f484d249c660418515fb01c2b9662073663c242e"
            },
            {
                "path": "alo.owl",
                "mode": "100755",
                "type": "blob",
                "size": 75,
                "sha": "45b983be36b73c0788dc9cbcb76cbb80fc7bb057",
                "url": "https://api.github.com/repos/octocat/Hello-World/git/blobs/45b983be36b73c0788dc9cbcb76cbb80fc7bb057"
            }
        ],
        "truncated": False
    }
    return tree

def get_fork_dict(repo):
    user, name = repo.split("/")
    fork = {
  "id": 1296269,
  "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
  "name": name,
  "full_name": repo,
  "owner": {
    "login": user,
    "id": 1,
    "node_id": "MDQ6VXNlcjE=",
    "avatar_url": "https://github.com/images/error/%s_happy.gif" % user,
    "gravatar_id": "",
    "url": "https://api.github.com/users/%s"% user,
    "html_url": "https://github.com/%s"% user,
    "followers_url": "https://api.github.com/users/%s/followers"% user,
    "following_url": "https://api.github.com/users/%s/following{/other_user}"% user,
    "gists_url": "https://api.github.com/users/%s/gists{/gist_id}"% user,
    "starred_url": "https://api.github.com/users/%s/starred{/owner}{/repo}"% user,
    "subscriptions_url": "https://api.github.com/users/%s/subscriptions"% user,
    "organizations_url": "https://api.github.com/users/%s/orgs"% user,
    "repos_url": "https://api.github.com/users/%s/repos"% user,
    "events_url": "https://api.github.com/users/%s/events{/privacy}"% user,
    "received_events_url": "https://api.github.com/users/%s/received_events"% user,
    "type": "User",
    "site_admin": False
  },
  "private": False,
  "html_url": "https://github.com/%s" % repo,
  "description": "This your first repo!",
  "fork": True,
  "url": "https://api.github.com/repos/%s"% repo,
  "archive_url": "http://api.github.com/repos/%s/{archive_format}{/ref}"% repo,
  "assignees_url": "http://api.github.com/repos/%s/assignees{/user}"% repo,
  "blobs_url": "http://api.github.com/repos/%s/git/blobs{/sha}"% repo,
  "branches_url": "http://api.github.com/repos/%s/branches{/branch}"% repo,
  "collaborators_url": "http://api.github.com/repos/%s/collaborators{/collaborator}"% repo,
  "comments_url": "http://api.github.com/repos/%s/comments{/number}"% repo,
  "commits_url": "http://api.github.com/repos/%s/commits{/sha}"% repo,
  "compare_url": "http://api.github.com/repos/%s/compare/{base}...{head}"% repo,
  "contents_url": "http://api.github.com/repos/%s/contents/{+path}"% repo,
  "contributors_url": "http://api.github.com/repos/%s/contributors"% repo,
  "deployments_url": "http://api.github.com/repos/%s/deployments"% repo,
  "downloads_url": "http://api.github.com/repos/%s/downloads"% repo,
  "events_url": "http://api.github.com/repos/%s/events"% repo,
  "forks_url": "http://api.github.com/repos/%s/forks"% repo,
  "git_commits_url": "http://api.github.com/repos/%s/git/commits{/sha}"% repo,
  "git_refs_url": "http://api.github.com/repos/%s/git/refs{/sha}"% repo,
  "git_tags_url": "http://api.github.com/repos/%s/git/tags{/sha}"% repo,
  "git_url": "git:github.com/%s.git"% repo,
  "issue_comment_url": "http://api.github.com/repos/%s/issues/comments{/number}"% repo,
  "issue_events_url": "http://api.github.com/repos/%s/issues/events{/number}"% repo,
  "issues_url": "http://api.github.com/repos/%s/issues{/number}"% repo,
  "keys_url": "http://api.github.com/repos/%s/keys{/key_id}"% repo,
  "labels_url": "http://api.github.com/repos/%s/labels{/name}"% repo,
  "languages_url": "http://api.github.com/repos/%s/languages"% repo,
  "merges_url": "http://api.github.com/repos/%s/merges"% repo,
  "milestones_url": "http://api.github.com/repos/%s/milestones{/number}"% repo,
  "notifications_url": "http://api.github.com/repos/%s/notifications{?since,all,participating}"% repo,
  "pulls_url": "http://api.github.com/repos/%s/pulls{/number}"% repo,
  "releases_url": "http://api.github.com/repos/%s/releases{/id}"% repo,
  "ssh_url": "git@github.com:%s.git"% repo,
  "stargazers_url": "http://api.github.com/repos/%s/stargazers"% repo,
  "statuses_url": "http://api.github.com/repos/%s/statuses/{sha}"% repo,
  "subscribers_url": "http://api.github.com/repos/%s/subscribers"% repo,
  "subscription_url": "http://api.github.com/repos/%s/subscription"% repo,
  "tags_url": "http://api.github.com/repos/%s/tags"% repo,
  "teams_url": "http://api.github.com/repos/%s/teams"% repo,
  "trees_url": "http://api.github.com/repos/%s/git/trees{/sha}"% repo,
  "clone_url": "https://github.com/%s.git"% repo,
  "mirror_url": "git:git.example.com/%s"% repo,
  "hooks_url": "http://api.github.com/repos/%s/hooks"% repo,
  "svn_url": "https://svn.github.com/%s"% repo,
  "homepage": "https://github.com",
  "language": None,
  "forks_count": 9,
  "stargazers_count": 80,
  "watchers_count": 80,
  "size": 108,
  "default_branch": "master",
  "open_issues_count": 0,
  "is_template": True,
  "topics": [
    "abc",
    "atom",
    "electron",
    "api"
  ],
  "has_issues": True,
  "has_projects": True,
  "has_wiki": True,
  "has_pages": False,
  "has_downloads": True,
  "archived": False,
  "disabled": False,
  "visibility": "public",
  "pushed_at": "2011-01-26T19:06:43Z",
  "created_at": "2011-01-26T19:01:12Z",
  "updated_at": "2011-01-26T19:14:43Z",
  "permissions": {
    "admin": False,
    "push": False,
    "pull": True
  },
  "allow_rebase_merge": True,
  "template_repository": None,
  "temp_clone_token": "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
  "allow_squash_merge": True,
  "delete_branch_on_merge": True,
  "allow_merge_commit": True,
  "subscribers_count": 42,
  "network_count": 0
}
    return fork


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
    }
}

mock_dict = {
    'success': mock_dict_success
}
