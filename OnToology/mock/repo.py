from .org import get_organization_dict


def get_license_dict():
    license = {
        "key": "mit",
        "name": "MIT License",
        "spdx_id": "MIT",
        "url": "https://api.github.com/licenses/mit",
        "node_id": "MDc6TGljZW5zZW1pdA==",
    }
    return license


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


def get_add_collaborator_dict(repo):
    user, repo_name = repo.split('/')
    coll_dict = {
      "id": 1,
      "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
      "repository": {
        "id": 1296269,
        "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
        "name": repo_name,
        "full_name": repo,
        "owner": {
          "login": user,
          "id": 1,
          "node_id": "MDQ6VXNlcjE=",
          "avatar_url": "https://github.com/images/error/octocat_happy.gif",
          "gravatar_id": "",
          "url": "https://api.github.com/users/%s" % (user),
          "html_url": "https://github.com/octocat",
          "followers_url": "https://api.github.com/users/octocat/followers",
          "following_url": "https://api.github.com/users/octocat/following{/other_user}",
          "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
          "organizations_url": "https://api.github.com/users/octocat/orgs",
          "repos_url": "https://api.github.com/users/octocat/repos",
          "events_url": "https://api.github.com/users/octocat/events{/privacy}",
          "received_events_url": "https://api.github.com/users/octocat/received_events",
          "type": "User",
          "site_admin": False
        },
        "private": False,
        "html_url": "https://github.com/%s" % repo,
        "description": "This your first repo!",
        "fork": False,
        "url": "https://api.github.com/repos/%s" % repo,
        "archive_url": "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
        "assignees_url": "https://api.github.com/repos/octocat/Hello-World/assignees{/user}",
        "blobs_url": "https://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
        "branches_url": "https://api.github.com/repos/octocat/Hello-World/branches{/branch}",
        "collaborators_url": "https://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
        "comments_url": "https://api.github.com/repos/octocat/Hello-World/comments{/number}",
        "commits_url": "https://api.github.com/repos/octocat/Hello-World/commits{/sha}",
        "compare_url": "https://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
        "contents_url": "https://api.github.com/repos/octocat/Hello-World/contents/{+path}",
        "contributors_url": "https://api.github.com/repos/octocat/Hello-World/contributors",
        "deployments_url": "https://api.github.com/repos/octocat/Hello-World/deployments",
        "downloads_url": "https://api.github.com/repos/octocat/Hello-World/downloads",
        "events_url": "https://api.github.com/repos/octocat/Hello-World/events",
        "forks_url": "https://api.github.com/repos/octocat/Hello-World/forks",
        "git_commits_url": "https://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
        "git_refs_url": "https://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
        "git_tags_url": "https://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
        "git_url": "git:github.com/%s.git" % repo,
        "issue_comment_url": "https://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
        "issue_events_url": "https://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
        "issues_url": "https://api.github.com/repos/octocat/Hello-World/issues{/number}",
        "keys_url": "https://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
        "labels_url": "https://api.github.com/repos/octocat/Hello-World/labels{/name}",
        "languages_url": "https://api.github.com/repos/octocat/Hello-World/languages",
        "merges_url": "https://api.github.com/repos/octocat/Hello-World/merges",
        "milestones_url": "https://api.github.com/repos/octocat/Hello-World/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}",
        "pulls_url": "https://api.github.com/repos/octocat/Hello-World/pulls{/number}",
        "releases_url": "https://api.github.com/repos/octocat/Hello-World/releases{/id}",
        "ssh_url": "git@github.com:%s.git" % repo,
        "stargazers_url": "https://api.github.com/repos/octocat/Hello-World/stargazers",
        "statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
        "subscribers_url": "https://api.github.com/repos/octocat/Hello-World/subscribers",
        "subscription_url": "https://api.github.com/repos/octocat/Hello-World/subscription",
        "tags_url": "https://api.github.com/repos/octocat/Hello-World/tags",
        "teams_url": "https://api.github.com/repos/octocat/Hello-World/teams",
        "trees_url": "https://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
        "hooks_url": "http://api.github.com/repos/octocat/Hello-World/hooks"
      },
      "invitee": {
        "login": user,
        "id": 1,
        "node_id": "MDQ6VXNlcjE=",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "",
        "url": "https://api.github.com/users/%s" % user,
        "html_url": "https://github.com/octocat",
        "followers_url": "https://api.github.com/users/octocat/followers",
        "following_url": "https://api.github.com/users/octocat/following{/other_user}",
        "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
        "organizations_url": "https://api.github.com/users/octocat/orgs",
        "repos_url": "https://api.github.com/users/octocat/repos",
        "events_url": "https://api.github.com/users/octocat/events{/privacy}",
        "received_events_url": "https://api.github.com/users/octocat/received_events",
        "type": "User",
        "site_admin": False
      },
      "inviter": {
        "login": user,
        "id": 1,
        "node_id": "MDQ6VXNlcjE=",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "",
        "url": "https://api.github.com/users/octocat",
        "html_url": "https://github.com/octocat",
        "followers_url": "https://api.github.com/users/octocat/followers",
        "following_url": "https://api.github.com/users/octocat/following{/other_user}",
        "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
        "organizations_url": "https://api.github.com/users/octocat/orgs",
        "repos_url": "https://api.github.com/users/octocat/repos",
        "events_url": "https://api.github.com/users/octocat/events{/privacy}",
        "received_events_url": "https://api.github.com/users/octocat/received_events",
        "type": "User",
        "site_admin": False
      },
      "permissions": "write",
      "created_at": "2016-06-13T14:52:50-05:00",
      "url": "https://api.github.com/user/repository_invitations/1296269",
      "html_url": "https://github.com/%s/invitations" % repo
    }
    return coll_dict


def get_file_content_dict(repo, branch, f_relative_dir):
    """
    :param repo: owner/repo_name
    :param branch: master
    :param f_relative_dir: e.g., OnToology/abc.conf
    :return:
    """
    sha = "3d21ec53a331a6f037a91c368710b99387d012c1"
    d = {
        "type": "file",
        "encoding": "base64",
        "size": 5362,
        "name": f_relative_dir.split('/')[-1],
        "path": f_relative_dir,
        "content": "encoded content ...",
        "sha": sha,
        "url": "https://api.github.com/repos/%s/contents/%s" % (repo, f_relative_dir) ,
        "git_url": "https://api.github.com/repos/%s/git/blobs/%s" %(repo, sha),
        "html_url": "https://github.com/%s/blob/%s/%s" % (repo, branch, f_relative_dir),
        "download_url": "https://raw.githubusercontent.com/%s/%s/%s" % (repo, branch, f_relative_dir),
        "_links": {
            "git": "https://api.github.com/repos/%s/git/blobs/%s" % (repo,sha),
            "self": "https://api.github.com/repos/%s/contents/%s" % (repo, f_relative_dir),
            "html": "https://github.com/%s/blob/%s/%s" % (repo, branch, f_relative_dir)
        }
    }
    return d

def get_update_content_dict(repo, branch, f_relative_dir):
    """
    Updating a file content
    :param repo: owner/repo_name
    :param branch: master
    :param f_relative_dir: e.g., OnToology/abc.conf

    :return:
    """
    sha = "a56507ed892d05a37c6d6128c260937ea4d287bd"
    d = {
        "content": {
            "name": f_relative_dir.split('/')[-1],
            "path": f_relative_dir,
            "sha": "%s" % sha,
            "size": 9,
            "url": "https://api.github.com/repos/%s/contents/%s" % (repo, f_relative_dir),
            "html_url": "https://github.com/%s/blob/%s/%s" % (repo, branch, f_relative_dir),
            "git_url": "https://api.github.com/repos/%s/git/blobs/%s" % (repo, sha),
            "download_url": "https://raw.githubusercontent.com/%s/%s/%s" % (repo, branch, f_relative_dir),
            "type": "file",
            "_links": {
                "self": "https://api.github.com/repos/%s/contents/%s" % (repo,f_relative_dir),
                "git": "https://api.github.com/repos/%s/git/blobs/%s" % (repo,sha),
                "html": "https://github.com/%s/blob/%s/%s" % (repo, branch, f_relative_dir)
            }
        },
        "commit": {
            "sha": "18a43cd8e1e3a79c786e3d808a73d23b6d212b16",
            "node_id": "MDY6Q29tbWl0MThhNDNjZDhlMWUzYTc5Yzc4NmUzZDgwOGE3M2QyM2I2ZDIxMmIxNg==",
            "url": "https://api.github.com/repos/octocat/Hello-World/git/commits/18a43cd8e1e3a79c786e3d808a73d23b6d212b16",
            "html_url": "https://github.com/octocat/Hello-World/git/commit/18a43cd8e1e3a79c786e3d808a73d23b6d212b16",
            "author": {
                "date": "2014-11-07T22:01:45Z",
                "name": "Monalisa Octocat",
                "email": "octocat@github.com"
            },
            "committer": {
                "date": "2014-11-07T22:01:45Z",
                "name": "Monalisa Octocat",
                "email": "octocat@github.com"
            },
            "message": "my commit message",
            "tree": {
                "url": "https://api.github.com/repos/octocat/Hello-World/git/trees/9a21f8e2018f42ffcf369b24d2cd20bc25c9e66f",
                "sha": "9a21f8e2018f42ffcf369b24d2cd20bc25c9e66f"
            },
            "parents": [
                {
                    "url": "https://api.github.com/repos/octocat/Hello-World/git/commits/da5a433788da5c255edad7979b328b67d79f53f6",
                    "html_url": "https://github.com/octocat/Hello-World/git/commit/da5a433788da5c255edad7979b328b67d79f53f6",
                    "sha": "da5a433788da5c255edad7979b328b67d79f53f6"
                }
            ],
            "verification": {
                "verified": False,
                "reason": "unsigned",
                "signature": None,
                "payload": None
            }
        }
    }
    return d