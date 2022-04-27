from .user import get_user_dict


def get_milestone_dict(repo):
    user, name = repo.split("/")
    milestone = {
      "url": "https://api.github.com/repos/%s/milestones/1" % repo,
      "html_url": "https://github.com/%s/milestones/v1.0" % repo,
      "labels_url": "https://api.github.com/repos/%s/milestones/1/labels" % repo,
      "id": 1002604,
      "node_id": "MDk6TWlsZXN0b25lMTAwMjYwNA==",
      "number": 1,
      "state": "open",
      "title": "v1.0",
      "description": "Tracking milestone for version 1.0",
      "creator": get_user_dict(user),
      "open_issues": 4,
      "closed_issues": 8,
      "created_at": "2011-04-10T20:09:31Z",
      "updated_at": "2014-03-03T18:58:10Z",
      "closed_at": "2013-02-12T13:22:01Z",
      "due_on": "2012-10-09T23:39:01Z"
    }
    return milestone