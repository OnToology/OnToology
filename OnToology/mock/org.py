

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