from .repo import get_repo_dict
from .user import get_user_dict
from .milestone import get_milestone_dict


def get_pulls_dict(repo, branch="master"):
  user, name = repo.split('/')
  pulls = [{
    "url": "https://api.github.com/repos/%s/pulls/1347" % repo,
    "id": 1,
    "node_id": "MDExOlB1bGxSZXF1ZXN0MQ==",
    "html_url": "https://github.com/%s/pull/1347"% repo,
    "diff_url": "https://github.com/%s/pull/1347.diff"% repo,
    "patch_url": "https://github.com/%s/pull/1347.patch"% repo,
    "issue_url": "https://api.github.com/repos/%s/issues/1347"% repo,
    "commits_url": "https://api.github.com/repos/%s/pulls/1347/commits"% repo,
    "review_comments_url": "https://api.github.com/repos/%s/pulls/1347/comments"% repo,
    "review_comment_url": "https://api.github.com/repos/%s/pulls/comments{/number}"% repo,
    "comments_url": "https://api.github.com/repos/%s/issues/1347/comments"% repo,
    "statuses_url": "https://api.github.com/repos/%s/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e"% repo,
    "number": 1347,
    "state": "open",
    "locked": True,
    "title": "Amazing new feature",
    "user": get_user_dict(user),
    "body": "Please pull these awesome changes in!",
    "labels": [
      {
        "id": 208045946,
        "node_id": "MDU6TGFiZWwyMDgwNDU5NDY=",
        "url": "https://api.github.com/repos/%s/labels/bug"% repo,
        "name": "bug",
        "description": "Something is not working",
        "color": "f29513",
        "default": True
      }
    ],
    "milestone": get_milestone_dict(repo),
    "active_lock_reason": "too heated",
    "created_at": "2011-01-26T19:01:12Z",
    "updated_at": "2011-01-26T19:01:12Z",
    "closed_at": "2011-01-26T19:01:12Z",
    "merged_at": "2011-01-26T19:01:12Z",
    "merge_commit_sha": "e5bd3914e2e596debea16f433f57875b5b90bcd6",
    "assignee": get_user_dict(user),
    "assignees": [
      get_user_dict(user)
    ],
    "requested_reviewers": [
      get_user_dict(user)
    ],
    "requested_teams": [
      {
        "id": 1,
        "node_id": "MDQ6VGVhbTE=",
        "url": "https://api.github.com/teams/1",
        "html_url": "https://api.github.com/teams/justice-league",
        "name": "Justice League",
        "slug": "justice-league",
        "description": "A great team.",
        "privacy": "closed",
        "permission": "admin",
        "members_url": "https://api.github.com/teams/1/members{/member}",
        "repositories_url": "https://api.github.com/teams/1/repos"
      }
    ],
    "head": {
      "label": "octocat:new-topic",
      "ref": "new-topic",
      "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
      "user": get_user_dict(user),
      "repo": get_repo_dict(repo)
    },
    "base": {
      "label": "octocat:%s" % branch,
      "ref": "%s" % branch,
      "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
      "user": get_user_dict(user),
      "repo": get_repo_dict(repo)
    },
    "_links": {
      "self": {
        "href": "https://api.github.com/repos/%s/pulls/1347"% repo
      },
      "html": {
        "href": "https://github.com/%s/pull/1347"% repo
      },
      "issue": {
        "href": "https://api.github.com/repos/%s/issues/1347"% repo
      },
      "comments": {
        "href": "https://api.github.com/repos/%s/issues/1347/comments"% repo
      },
      "review_comments": {
        "href": "https://api.github.com/repos/%s/pulls/1347/comments"% repo
      },
      "review_comment": {
        "href": "https://api.github.com/repos/%s/pulls/comments{/number}"% repo
      },
      "commits": {
        "href": "https://api.github.com/repos/%s/pulls/1347/commits"% repo
      },
      "statuses": {
        "href": "https://api.github.com/repos/%s/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e"% repo
      }
    },
    "author_association": "OWNER",
    "draft": False
  }
]
  return pulls

