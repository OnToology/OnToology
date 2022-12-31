from .user import get_auth_user_dict


def get_commits_dict(repo):
    # user, name = repo.split("/")
    user, _ = repo.split("/")
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















